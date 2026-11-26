
import requests
import time
from datetime import datetime

print("=== ATACANTE NORMAL ===")

IP_ALVO = input("Digite o IP do servidor alvo: ").strip()
SERVIDOR = f"http://{IP_ALVO}:5000"

print(f"\nAlvo definido: {SERVIDOR}")
print("Simulando usuario legitimo...\n")

for i in range(10):

    try:
        resposta = requests.get(SERVIDOR, timeout=5)

        horario = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{horario}] "
            f"Requisicao {i + 1}/10 | "
            f"HTTP {resposta.status_code}"
        )

    except requests.exceptions.RequestException as erro:
        print(f"Erro de conexao: {erro}")
        break

    time.sleep(3)

print("\nSimulacao normal finalizada.")
