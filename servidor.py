
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
from motor_score import MotorScore

app = Flask(__name__)
motor = MotorScore()


# ==========================================
# MONITORAMENTO E BLOQUEIO
# ==========================================

@app.before_request
def analisar_requisicao():

    ip = request.remote_addr
    horario = datetime.now().strftime("%H:%M:%S")

    # Verifica se o IP ja esta bloqueado
    if motor.esta_bloqueado(ip):
        print(f"[BLOQUEIO] IP {ip} recusado!")
        return jsonify({
            "status": "bloqueado",
            "ip": ip,
            "mensagem": "Acesso recusado pelo sistema antifraude."
        }), 403

    # Consultas do dashboard nao geram pontuacao
    if request.path in ["/dashboard", "/api/estado", "/atacar", "/favicon.ico"]:
        return None

    # Analisa o comportamento do IP
    resultado = motor.registrar_requisicao(ip)

    print(
        f"[{horario}] "
        f"IP: {ip} | "
        f"Requisicoes: {resultado['requisicoes_janela']} | "
        f"Score: {resultado['score']} | "
        f"Decisao: {resultado['decisao']}"
    )

    if resultado["decisao"] == "BLOQUEAR":
        print(f"[BLOQUEIO] IP {ip} recusado!")

        return jsonify({
            "status": "bloqueado",
            "ip": ip,
            "mensagem": "Acesso recusado pelo sistema antifraude."
        }), 403


# ==========================================
# PAGINA INICIAL
# ==========================================

@app.route("/", methods=["GET"])
def inicio():

    return jsonify({
        "sistema": "Detector de Fraudes",
        "status": "online",
        "mensagem": "Sistema de protecao ativo!"
    })


# ==========================================
# API DE MONITORAMENTO
# ==========================================

@app.route("/api/estado", methods=["GET"])
def consultar_estado():

    return jsonify(motor.consultar_estado())


# ==========================================
# DASHBOARD WEB
# ==========================================

@app.route("/dashboard", methods=["GET"])
def dashboard():

    html = """
    <!DOCTYPE html>
    <html lang="pt-br">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Detector de Fraudes | Dashboard</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 30px;
                background: #10151f;
                color: #e5e7eb;
                font-family: Arial, sans-serif;
            }

            header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 15px;
                margin-bottom: 30px;
            }

            h1 {
                margin: 0;
                font-size: 26px;
            }

            .subtitulo {
                color: #9ca3af;
                margin-top: 8px;
            }

            .status {
                color: #4ade80;
                font-weight: bold;
            }

            .cards {
                display: grid;
                grid-template-columns: repeat(
                    auto-fit, minmax(180px, 1fr)
                );
                gap: 18px;
                margin-bottom: 30px;
            }

            .card {
                background: #1c2533;
                padding: 22px;
                border-radius: 10px;
                border: 1px solid #303c4e;
            }

            .card h3 {
                color: #9ca3af;
                font-size: 13px;
                margin: 0 0 12px;
            }

            .numero {
                font-size: 30px;
                font-weight: bold;
            }

            .painel {
                background: #1c2533;
                padding: 22px;
                border-radius: 10px;
                border: 1px solid #303c4e;
                overflow-x: auto;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
                min-width: 600px;
            }

            th, td {
                padding: 15px 12px;
                text-align: left;
                border-bottom: 1px solid #303c4e;
            }

            th {
                color: #9ca3af;
                font-size: 12px;
                text-transform: uppercase;
            }

            .badge {
                padding: 6px 10px;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }

            .normal {
                background: #14532d;
                color: #86efac;
            }

            .suspeito {
                background: #713f12;
                color: #fde047;
            }

            .bloqueado {
                background: #7f1d1d;
                color: #fca5a5;
            }

            .barra {
                width: 100%;
                height: 8px;
                background: #374151;
                border-radius: 10px;
                overflow: hidden;
                margin-top: 7px;
            }

            .progresso {
                height: 100%;
                background: #38bdf8;
            }

            .rodape {
                margin-top: 20px;
                color: #6b7280;
                font-size: 12px;
            }
        </style>
    </head>

    <body>

        <header>
            <div>
                <h1>DETECTOR DE FRAUDES</h1>
                <div class="subtitulo">
                    Central de monitoramento e analise de IPs
                </div>
            </div>

            <div class="status">
                ● SISTEMA ONLINE
            </div>
        </header>

        <section class="cards">

            <div class="card">
                <h3>IPS MONITORADOS</h3>
                <div class="numero" id="total-ips">0</div>
            </div>

            <div class="card">
                <h3>IPS NORMAIS</h3>
                <div class="numero" id="total-normais">0</div>
            </div>

            <div class="card">
                <h3>IPS SUSPEITOS</h3>
                <div class="numero" id="total-suspeitos">0</div>
            </div>

            <div class="card">
                <h3>IPS BLOQUEADOS</h3>
                <div class="numero" id="total-bloqueados">0</div>
            </div>

        </section>

        <section class="painel">

            <h2>Monitoramento de origens</h2>

            <table>
                <thead>
                    <tr>
                        <th>Endereco IP</th>
                        <th>Requisicoes</th>
                        <th>Score</th>
                        <th>Classificacao</th>
                    </tr>
                </thead>

                <tbody id="tabela-ips">
                    <tr>
                        <td colspan="4">Aguardando dados...</td>
                    </tr>
                </tbody>
            </table>

            <div class="rodape" id="atualizacao">
                Aguardando primeira atualizacao...
            </div>

        </section>

        <script>

            async function atualizarDashboard() {

                try {

                    const resposta = await fetch("/api/estado");
                    const dados = await resposta.json();

                    const scores = dados.scores || {};
                    const requisicoes = dados.requisicoes || {};
                    const bloqueados = dados.bloqueados || [];

                    const ips = Object.keys(scores);

                    let normais = 0;
                    let suspeitos = 0;
                    let totalBloqueados = 0;

                    let linhas = "";

                    ips.forEach(ip => {

                        const score = scores[ip];
                        const quantidade = requisicoes[ip] || 0;

                        let classificacao;
                        let classe;

                        if (bloqueados.includes(ip)) {

                            classificacao = "BLOQUEADO";
                            classe = "bloqueado";
                            totalBloqueados++;

                        } else if (score >= 30) {

                            classificacao = "SUSPEITO";
                            classe = "suspeito";
                            suspeitos++;

                        } else {

                            classificacao = "NORMAL";
                            classe = "normal";
                            normais++;

                        }

                        const barra = Math.min(score, 100);

                        linhas += `
                            <tr>
                                <td>${ip}</td>
                                <td>${quantidade}</td>
                                <td>
                                    ${score.toFixed(0)}
                                    <div class="barra">
                                        <div class="progresso"
                                             style="width: ${barra}%">
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    <span class="badge ${classe}">
                                        ${classificacao}
                                    </span>
                                </td>
                            </tr>
                        `;

                    });

                    document.getElementById("total-ips").textContent =
                        ips.length;

                    document.getElementById("total-normais").textContent =
                        normais;

                    document.getElementById("total-suspeitos").textContent =
                        suspeitos;

                    document.getElementById("total-bloqueados").textContent =
                        totalBloqueados;

                    document.getElementById("tabela-ips").innerHTML =
                        linhas || `
                            <tr>
                                <td colspan="4">
                                    Nenhuma atividade registrada.
                                </td>
                            </tr>
                        `;

                    document.getElementById("atualizacao").textContent =
                        "Ultima atualizacao: " +
                        new Date().toLocaleTimeString("pt-BR");

                } catch (erro) {

                    document.getElementById("atualizacao").textContent =
                        "Erro ao consultar o servidor.";

                }

            }

            atualizarDashboard();

            setInterval(atualizarDashboard, 2000);

        </script>

    </body>
    </html>
    """

    return render_template_string(html)


# ==========================================
# SIMULADOR DE ATAQUE PELO NAVEGADOR (celular)
# Abra http://IP_DO_SERVIDOR:5000/atacar no celular.
# As requisicoes saem do IP do proprio celular.
# ==========================================

@app.route("/atacar", methods=["GET"])
def atacar():

    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simulador de Ataques</title>
        <style>
            * { box-sizing: border-box; }
            body { margin: 0; padding: 20px; background: #10151f; color: #e5e7eb;
                   font-family: Arial, sans-serif; }
            h1 { font-size: 22px; margin: 0 0 4px; }
            .sub { color: #9ca3af; font-size: 13px; margin-bottom: 20px; }
            button { width: 100%; padding: 18px; margin-bottom: 12px; border: 0;
                     border-radius: 10px; font-size: 17px; font-weight: bold; color: #fff; }
            button:disabled { opacity: .4; }
            .b1 { background: #15803d; } .b2 { background: #b45309; } .b3 { background: #b91c1c; }
            .parar { background: #374151; }
            .info { font-size: 12px; font-weight: normal; display: block; margin-top: 4px; opacity: .85; }
            #status { padding: 14px; border-radius: 10px; background: #1c2533;
                      border: 1px solid #303c4e; margin: 8px 0 12px; font-weight: bold; }
            #log { background: #0b0f16; border-radius: 10px; padding: 12px; height: 260px;
                   overflow-y: auto; font-family: monospace; font-size: 13px; }
            .ok { color: #86efac; } .bloq { color: #fca5a5; font-weight: bold; } .err { color: #fde047; }
        </style>
    </head>
    <body>
        <h1>SIMULADOR DE ATAQUES</h1>
        <div class="sub">Requisicoes saem deste aparelho para o servidor</div>

        <button class="b1" onclick="iniciar('NORMAL', 10, 3000)">1 - NORMAL
            <span class="info">10 requisicoes, 1 a cada 3 s</span></button>
        <button class="b2" onclick="iniciar('SUSPEITO', 15, 1000)">2 - SUSPEITO
            <span class="info">15 requisicoes, 1 a cada 1 s</span></button>
        <button class="b3" onclick="iniciar('AGRESSIVO', 20, 200)">3 - AGRESSIVO
            <span class="info">20 requisicoes, 1 a cada 0,2 s</span></button>
        <button class="parar" onclick="parar()">PARAR</button>

        <div id="status">Escolha um perfil.</div>
        <div id="log"></div>

        <script>
            let rodando = false;
            const espera = ms => new Promise(r => setTimeout(r, ms));
            const log = (txt, cls) => {
                const el = document.getElementById("log");
                el.innerHTML += `<div class="${cls}">${txt}</div>`;
                el.scrollTop = el.scrollHeight;
            };
            const status = txt => document.getElementById("status").textContent = txt;
            const botoes = on => document.querySelectorAll("button:not(.parar)")
                .forEach(b => b.disabled = !on);

            function parar() { rodando = false; }

            async function iniciar(nome, total, intervalo) {
                rodando = true; botoes(false);
                document.getElementById("log").innerHTML = "";
                status("Perfil " + nome + " em execucao...");
                for (let i = 1; i <= total && rodando; i++) {
                    const hora = new Date().toLocaleTimeString("pt-BR");
                    try {
                        const r = await fetch("/?t=" + Date.now(), { cache: "no-store" });
                        if (r.status === 403) {
                            log(`[${hora}] Requisicao ${i}/${total} | HTTP 403`, "bloq");
                            status("BLOQUEIO CONFIRMADO: o servidor recusou o acesso.");
                            rodando = false; break;
                        }
                        log(`[${hora}] Requisicao ${i}/${total} | HTTP ${r.status}`, "ok");
                    } catch (e) {
                        log(`[${hora}] Erro de conexao`, "err");
                        status("Erro de conexao com o servidor."); rodando = false; break;
                    }
                    if (i < total) await espera(intervalo);
                    if (i === total) status("Perfil " + nome + " finalizado.");
                }
                if (!document.getElementById("status").textContent.startsWith("BLOQUEIO")
                    && !document.getElementById("status").textContent.startsWith("Erro")
                    && !document.getElementById("status").textContent.endsWith("finalizado."))
                    status("Simulacao interrompida.");
                rodando = false; botoes(true);
            }
        </script>
    </body>
    </html>
    """

    return render_template_string(html)


# ==========================================
# INICIALIZACAO
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print(" SISTEMA DE DETECCAO E BLOQUEIO")
    print(" Motor de pontuacao ativo!")
    print(" Dashboard: http://localhost:5000/dashboard")
    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )