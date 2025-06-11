# 📌 Sistemas Embarcados

## 📖 Sobre a Disciplina
Sistemas embarcados são dispositivos computacionais projetados para desempenhar funções específicas dentro de um sistema maior. Eles estão presentes em diversas áreas, como automação industrial, eletrônicos de consumo, automóveis e dispositivos médicos.

## 📖 Sobre o Projeto
Este projeto visa auxiliar a criação de estufas inteligentes por meio do monitoramento em tempo real da temperatura e umidade utilizando um ESP32, sensor DHT11, display OLED e comunicação via MQTT. Os dados coletados são exibidos localmente e enviados para um painel web, permitindo o acompanhamento remoto das condições ambientais. Além disso, o sistema dispara alertas automáticos via Telegram quando os limites de temperatura são excedidos, promovendo maior segurança e automação.

## 👥 Integrantes
- Beatriz Turi Pinto de Araujo - [LinkedIn](https://linkedin.com/in/beatrizturi)
- Lucas Fernandes Mosqueira - [LinkedIn](https://linkedin.com/in/lucas-fernandes-mosqueira)
- Lucas José Silva Serejo - [LinkedIn](https://linkedin.com/in/lucasjserejo)

## ⚙️ Funcionalidades

- **Leitura de Temperatura e Umidade:** Utiliza sensor DHT11 conectado ao ESP32.
- **Exibição Local:** Mostra os dados em um display OLED.
- **Envio de Dados via MQTT:** Publica métricas e alertas em tópicos específicos.
- **Monitoramento em Tempo Real:** Painel web (Streamlit) exibe métricas, gráficos e estatísticas de latência.
- **Alertas via Telegram:** Usuários podem se registrar para receber notificações automáticas.
- **Registro de Latência:** Mede e armazena o tempo entre o envio do dado pelo ESP32 e o recebimento no servidor e/ou envio ao Telegram.

## 📖 Avaliação Quantitativa de Desempenho

O sistema implementa duas métricas de latência para avaliação quantitativa do desempenho:

- **Latência ESP32 → Servidor Python:**  
  Mede o tempo entre o dado ser captado pelo ESP32 e o recebimento pelo backend Python via MQTT.  
  - **Definição:** `latência = timestamp_recebido - timestamp_esp32`
  - **Arquivo:** `latencia_esp32_server.csv`
  - **Painel:** `metrics_eval.py`
  - **Uso:** Avalia a eficiência da comunicação entre o dispositivo e o servidor.

- **Latência ESP32 → Telegram:**  
  Mede o tempo entre o dado ser captado pelo ESP32 e o envio da mensagem de alerta ao Telegram (após confirmação da API).  
  - **Definição:** `latência = timestamp_envio_telegram - timestamp_esp32`
  - **Arquivo:** `latencia_esp32_telegram.csv`
  - **Painel:** `metrics_eval_2.py`
  - **Uso:** Avalia o tempo total até o alerta ser encaminhado ao usuário via Telegram.

> **Observação:**  
> A latência ESP32 → Telegram não inclui o tempo até o usuário visualizar a mensagem, apenas até o envio ao Telegram.

## 🗂 Estrutura dos Arquivos

- `AP1/ESP32.ino`  
  Código para ESP32: leitura do sensor, exibição no display, envio MQTT.

- `AP1/main.py`  
  Backend Python: recebe dados MQTT, envia alertas Telegram, registra métricas de latência.

- `AP1/latencia_esp32_server.csv`  
  Arquivo CSV com registros de latência do ESP32 até o servidor Python.

- `AP1/latencia_esp32_telegram.csv`  
  Arquivo CSV com registros de latência do ESP32 até o envio ao Telegram.

- `AP1/metrics_eval.py`  
  Painel Streamlit para visualização em tempo real das métricas ESP32 → Servidor.

- `AP1/metrics_eval_2.py`  
  Painel Streamlit para visualização em tempo real das métricas ESP32 → Telegram.

- `AP1/users.json`  
  Lista de usuários registrados para receber alertas no Telegram.

## 🚀 Como Executar

1. **Configurar o ESP32**
   - Preencha as credenciais WiFi e carregue o código `ESP32.ino` no seu ESP32.
   - Conecte o sensor DHT11 e o display OLED conforme indicado no código.

2. **Rodar o Backend Python**
   - Instale as dependências:  
     `pip install paho-mqtt requests`
   - Preencha o token do Telegram em `main.py`.
   - Execute:  
     `python main.py`

3. **Visualizar o Painel de Métricas**
   - Instale as dependências:  
     `pip install streamlit pandas numpy`
   - Execute para o painel ESP32 → Servidor:  
     `streamlit run metrics_eval.py`
   - Execute para o painel ESP32 → Telegram:  
     `streamlit run metrics_eval_2.py`

4. **Receber Alertas no Telegram**
   - Inicie uma conversa com o bot do Telegram e envie qualquer mensagem para ser registrado.

---

Projeto desenvolvido para a disciplina de Sistemas Embarcados.