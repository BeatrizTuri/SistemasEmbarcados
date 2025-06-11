import streamlit as st
import pandas as pd
import numpy as np
import time
import os

CSV_FILE = "latencia_esp32_server.csv"

st.set_page_config(page_title="Monitoramento Latência ESP32", layout="wide")

st.title("📡 Monitoramento em Tempo Real - ESP32 → Servidor Python")
st.markdown("""
Este painel exibe as métricas de latência, temperatura e umidade registradas **do momento em que o dado é captado pelo ESP32 até o recebimento pelo servidor Python** via MQTT.

**Definição:**  
Latência = `timestamp_recebido` − `timestamp_esp32`  
Ou seja, o tempo entre o dado ser captado pelo sensor no ESP32 e o instante em que a mensagem chega ao backend Python.

**Observação:**  
Esta métrica **não inclui** o tempo de envio ao Telegram nem o tempo até o usuário visualizar a mensagem. Ela representa apenas o tempo de propagação do dado do dispositivo até o servidor.
""")

placeholder = st.empty()
refresh_interval = 2

while True:
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)

            df["timestamp_esp32"] = pd.to_datetime(df["timestamp_esp32"], unit="s")
            df["timestamp_recebido"] = pd.to_datetime(df["timestamp_recebido"], unit="s")
            df = df.sort_values("timestamp_recebido", ascending=False)

            # === Cálculo das métricas ===
            latencias = df["latencia_segundos"]
            erro_medio = latencias.mean()
            erro_quad_medio = np.mean(latencias**2)
            raiz_erro_quad_medio = np.sqrt(erro_quad_medio)

            with placeholder.container():
                st.subheader("📈 Últimos Registros")
                st.dataframe(df, use_container_width=True)

                st.subheader("📊 Métricas de Latência")
                col1, col2, col3 = st.columns(3)
                col1.metric(
                    label="Erro Médio (ME)",
                    value=f"{erro_medio:.3f} s",
                    help="Média das latências medidas. Indica o desvio médio em relação à latência ideal (zero)."
                )
                col2.metric(
                    label="Erro Quadrático Médio (MSE)",
                    value=f"{erro_quad_medio:.3f} s²",
                    help="Média dos quadrados dos erros. Penaliza mais os picos altos de latência."
                )
                col3.metric(
                    label="Raiz do Erro Quadrático Médio (RMSE)",
                    value=f"{raiz_erro_quad_medio:.3f} s",
                    help="Raiz quadrada do MSE. Indica a latência média considerando a penalização de picos."
                )

                st.subheader("📈 Latência ao Longo do Tempo")
                st.line_chart(df.sort_values("timestamp_recebido")[["latencia_segundos"]])

                st.subheader("🌡 Temperatura e 💧 Umidade")
                st.line_chart(df.sort_values("timestamp_recebido")[["temperatura", "umidade"]])
        except Exception as e:
            st.warning(f"Erro ao ler CSV: {e}")
    else:
        st.info("Aguardando o arquivo de métricas...")

    time.sleep(refresh_interval)
