import streamlit as st
import pandas as pd
import time
import os

CSV_FILE = "latencia_esp32_telegram.csv"

st.set_page_config(page_title="Monitoramento Latência ESP32", layout="wide")

st.title("📡 Monitoramento em Tempo Real - ESP32 ↔ Telegram")
st.markdown("Este painel exibe métricas de latência, temperatura e umidade registradas em tempo real.")

# Área principal com auto-atualização
placeholder = st.empty()

# Intervalo de atualização (em segundos)
refresh_interval = 2

while True:
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)

            df["timestamp_esp32"] = pd.to_datetime(df["timestamp_esp32"], unit="s")
            df["timestamp_recebido"] = pd.to_datetime(df["timestamp_recebido"], unit="s")

            df = df.sort_values("timestamp_recebido", ascending=False)

            with placeholder.container():
                st.subheader("📈 Últimos Registros")
                st.dataframe(df, use_container_width=True)

                st.subheader("📊 Latência ao Longo do Tempo")
                st.line_chart(df.sort_values("timestamp_recebido")[["latencia_segundos"]])

                st.subheader("🌡 Temperatura e 💧 Umidade")
                st.line_chart(df.sort_values("timestamp_recebido")[["temperatura", "umidade"]])
        except Exception as e:
            st.warning(f"Erro ao ler CSV: {e}")
    else:
        st.info("Aguardando o arquivo de métricas...")

    time.sleep(refresh_interval)
