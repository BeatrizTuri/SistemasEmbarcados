# 📌 Sistemas Embarcados

## 📖 Sobre a Disciplina
Sistemas embarcados são dispositivos computacionais projetados para desempenhar funções específicas dentro de um sistema maior. Eles estão presentes em diversas áreas, como automação industrial, eletrônicos de consumo, automóveis e dispositivos médicos.

## 📖 Sobre o Projeto

Este projeto demonstra um sistema embarcado de monitoramento de temperatura e umidade utilizando ESP32, sensor DHT11, display OLED e comunicação via MQTT. Os dados coletados são enviados para um painel de monitoramento em tempo real e alertas são disparados via Telegram quando limites de temperatura são excedidos.

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
- **Registro de Latência:** Mede e armazena o tempo entre o envio do dado pelo ESP32 e o recebimento no servidor.

## 🗂 Estrutura dos Arquivos

- `AP1/ESP32.ino`  
  Código para ESP32: leitura do sensor, exibição no display, envio MQTT.

- `AP1/main.py`  
  Backend Python: recebe dados MQTT, envia alertas Telegram, registra métricas de latência.

- `AP1/latencia_esp32_telegram.csv`  
  Arquivo CSV onde são salvos os registros de latência, temperatura e umidade.

- `AP1/metrics_eval.py`  
  Painel Streamlit para visualização em tempo real das métricas e gráficos.

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
   - Execute:  
     `streamlit run metrics_eval.py`

4. **Receber Alertas no Telegram**
   - Inicie uma conversa com o bot do Telegram e envie qualquer mensagem para ser registrado.
---

Projeto desenvolvido para a disciplina de Sistemas Embarcados.