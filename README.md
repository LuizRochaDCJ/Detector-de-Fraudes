# Sistemas de Reputação e Detecção de Fraude

Projeto acadêmico de detecção de comportamentos suspeitos por meio de análise de reputação de endereços IP.

## Objetivo

O sistema monitora as requisições recebidas por um servidor e atribui uma pontuação de reputação a cada endereço IP. Com base no comportamento identificado, classifica os dispositivos como normais, suspeitos ou bloqueados.

## Tecnologias utilizadas

- Python
- Flask
- Requests
- HTML, CSS e JavaScript

## Funcionalidades

- Monitoramento de requisições HTTP.
- Cálculo de pontuação de reputação por endereço IP.
- Identificação de comportamentos suspeitos.
- Bloqueio automático de endereços IP que ultrapassam o limite estabelecido.
- Dashboard para acompanhamento em tempo real.
- Simulação de diferentes perfis de comportamento.

## Instalação e execução — Windows

### 1. Pré-requisitos

- Python 3 instalado.
- Os arquivos do projeto baixados no computador.
- Os dispositivos conectados à mesma rede Wi-Fi.

### 2. Instalar as dependências

Abra o terminal na pasta do projeto e execute:

```bash
python -m pip install -r requirements.txt
```

### 3. Iniciar o servidor

Execute:

```bash
python servidor.py
```

O servidor ficará disponível na porta 5000.

### 4. Acessar o dashboard

Em um navegador, acesse:

http://IP_DO_SERVIDOR:5000/dashboard

Substitua IP_DO_SERVIDOR pelo endereço IPv4 local do computador que está executando o servidor.

### 5. Executar uma simulação

Em outro computador conectado à mesma rede, execute um dos scripts:

```bash
python atacante_normal.py
```

```bash
python atacante_suspeito.py
```

```bash
python atacante_agressivo.py
```

Informe o IP do servidor quando solicitado e acompanhe os resultados no dashboard.

## Instalação e execução — Android (Termux)

### 1. Pré-requisitos

- Celular Android.
- Aplicativo Termux instalado.
- Arquivo `atacante_android.py` baixado na pasta `Downloads` do celular.
- Celular e servidor conectados à mesma rede Wi-Fi.

### 2. Preparar o Termux

Abra o Termux e execute:

```bash
pkg update && pkg upgrade
```

Instale o Python:

```bash
pkg install python
```

Instale a biblioteca Requests:

```bash
python -m pip install requests
```

### 3. Permitir acesso aos arquivos do Android

Execute o comando:

```bash
termux-setup-storage
```

O Android exibirá uma solicitação de permissão. Autorize o acesso aos arquivos.

Esse procedimento permite que o Termux acesse as pastas compartilhadas do armazenamento do celular.

### 4. Acessar a pasta Downloads

No Termux, execute:

```bash
cd ~/storage/downloads
```

Esse comando direciona o terminal para a pasta padrão `Downloads` do Android.

Para conferir se o arquivo está disponível, execute:

```bash
ls
```

Verifique se `atacante_android.py` aparece na listagem.

### 5. Executar o simulador

Ainda dentro da pasta Downloads, execute:

```bash
python atacante_android.py
```

### 6. Selecionar o perfil de simulação

O programa apresenta três opções:

- **1 — Normal:** simula 10 requisições, com intervalo de 3 segundos.
- **2 — Suspeito:** simula 15 requisições, com intervalo de 1 segundo.
- **3 — Agressivo:** simula 20 requisições, com intervalo de 0,2 segundo.

### 7. Informar o servidor

Digite o endereço IPv4 local do computador que está executando o servidor.

O programa enviará as requisições e exibirá os códigos HTTP recebidos. Caso o servidor bloqueie o dispositivo, o simulador identificará a resposta HTTP 403 e encerrará a execução.


## Segurança e condições de uso

Este projeto foi desenvolvido para fins acadêmicos e demonstrações controladas.

- Execute os testes somente em dispositivos próprios ou com autorização expressa dos responsáveis.
- Realize as simulações exclusivamente em redes privadas e controladas.
- Não exponha o servidor diretamente à internet.
- Mantenha o servidor e os dispositivos simuladores conectados à mesma rede Wi-Fi.
- Verifique se o roteador permite a comunicação entre dispositivos conectados à rede (sem isolamento de clientes).

### Demonstração em rede offline

O GitHub exige conexão com a internet. Portanto, antes da demonstração:

1. Baixe o projeto e seus arquivos enquanto houver acesso à internet.
2. Prepare os computadores e celulares que serão utilizados.
3. Conecte todos os dispositivos à mesma rede Wi-Fi privada.
4. Inicie o servidor no computador responsável pelo monitoramento.
5. Execute os simuladores nos demais dispositivos utilizando o IP local do servidor.

**Importante:** a rede utilizada na demonstração pode funcionar sem acesso à internet, desde que permita a comunicação local entre os dispositivos.
