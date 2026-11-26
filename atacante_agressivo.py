
import requests
import time
from datetime import datetime

print("=== ATACANTE AGRESSIVO ===")

IP_ALVO = input("Digite o IP do servidor alvo: ").strip()
SERVIDOR = f"http://{IP_ALVO}:5000"

print(f"\nAlvo definido: {SERVIDOR}")
print("Iniciando teste de frequencia elevada...\n")

for i in range(20):

    try:
        resposta = requests.get(SERVIDOR, timeout=5)

        horario = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{horario}] "
            f"Requisicao {i + 1}/20 | "
            f"HTTP {resposta.status_code}"
        )

        if resposta.status_code == 403:
            print("\n[BLOQUEIO CONFIRMADO] O servidor recusou o acesso.")
            break

    except requests.exceptions.RequestException as erro:
        print(f"Erro de conexao: {erro}")
        break

    time.sleep(0.2)

print("\nTeste agressivo finalizado.")
