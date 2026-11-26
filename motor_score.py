

from collections import defaultdict, deque
from datetime import datetime
import threading




class MotorScore:


    def __init__(self):
        self.eventos_ip = defaultdict(deque)
        self.scores_ip = defaultdict(float)
        self.ultima_atividade = {}
        self.bloqueados = set()
        self.lock = threading.Lock()


        self.janela_segundos = 30
        self.intervalo_decaimento = 10
        self.pontos_decaimento = 5


        self.limite_suspeito = 30
        self.limite_bloqueio = 60


    def registrar_requisicao(self, ip):


        agora = datetime.now()


        with self.lock:


            eventos = self.eventos_ip[ip]


            # Remove requisicoes antigas da janela
            while eventos and (agora - eventos[0]).total_seconds() > self.janela_segundos:
                eventos.popleft()


            # Aplica decaimento desde a ultima atividade
            ultima = self.ultima_atividade.get(ip)


            if ultima:
                tempo_parado = (agora - ultima).total_seconds()
                intervalos = int(tempo_parado // self.intervalo_decaimento)


                if intervalos > 0:
                    reducao = intervalos * self.pontos_decaimento
                    self.scores_ip[ip] = max(
                        0, self.scores_ip[ip] - reducao
                    )


            self.ultima_atividade[ip] = agora


            # Registra a nova requisicao
            eventos.append(agora)


            quantidade = len(eventos)


            # Pontuacao por frequencia
            if quantidade > 10:
                self.scores_ip[ip] += 5
            elif quantidade > 5:
                self.scores_ip[ip] += 4


            self.scores_ip[ip] = min(self.scores_ip[ip], 100)


            score = self.scores_ip[ip]


            # Classificacao
            if score >= self.limite_bloqueio:
                decisao = "BLOQUEAR"
                self.bloqueados.add(ip)


            elif score >= self.limite_suspeito:
                decisao = "SUSPEITO"


            else:
                decisao = "NORMAL"


            return {
                "ip": ip,
                "requisicoes_janela": quantidade,
                "score": score,
                "decisao": decisao
            }


    def esta_bloqueado(self, ip):


        with self.lock:
            return ip in self.bloqueados


    def consultar_estado(self):


        with self.lock:
            return {
                "scores": dict(self.scores_ip),
                "bloqueados": list(self.bloqueados),
                "requisicoes": {
                    ip: len(eventos)
                    for ip, eventos in self.eventos_ip.items()
                }
            }