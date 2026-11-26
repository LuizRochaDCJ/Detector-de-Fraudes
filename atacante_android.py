import requests
import time
from datetime import datetime

print("=" * 40)
print("       SIMULADOR DE ATAQUES")
print("=" * 40)

print("\nSelecione o perfil:")
print("[1] Atacante Normal")
print("[2] Atacante Suspeito")
print("[3] Atacante Agressivo")

opcao = input("\nDigite sua opcao: ").strip()

perfis = {
    "1": {
        "nome": "NORMAL",
        "requisicoes": 10,
        "intervalo": 3
    },
    "2": {
        "nome": "SUSPEITO",
        "requisicoes": 15,
        "intervalo": 1
    },
    "3": {
        "nome": "AGRESSIVO",
        "requisicoes": 20,
        "intervalo": 0.2
    }
}

if opcao not in perfis:
    print("\nOpcao invalida!")
    raise SystemExit

perfil = perfis[opcao]

ip_alvo = input("\nDigite o IP do servidor: ").strip()

if not ip_alvo:
    print("IP nao informado!")
    raise SystemExit

servidor = f"http://{ip_alvo}:5000"

print("\n" + "=" * 40)
print(f"PERFIL: {perfil['nome']}")
print(f"ALVO: {servidor}")
print("=" * 40)

confirmacao = input("\nIniciar simulacao? (s/n): ").strip().lower()

if confirmacao != "s":
    print("Simulacao cancelada.")
    raise SystemExit

print("\nIniciando simulacao...\n")

for i in range(perfil["requisicoes"]):

    try:
        resposta = requests.get(servidor, timeout=5)

        horario = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{horario}] "
            f"Requisicao {i + 1}/{perfil['requisicoes']} "
            f"| HTTP {resposta.status_code}"
        )

        if resposta.status_code == 403:
            print("\n[BLOQUEIO CONFIRMADO]")
            print("O servidor recusou o acesso.")
            break

    except requests.exceptions.RequestException as erro:
        print(f"\nErro de conexao: {erro}")
        break

    if i < perfil["requisicoes"] - 1:
        time.sleep(perfil["intervalo"])

print("\nSimulacao finalizada.")