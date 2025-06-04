import streamlit as st
import pandas as pd
import numpy as np
import time
import os

CSV_FILE = "latencia_esp32_telegram.csv"

st.set_page_config(page_title="Monitoramento Latência ESP32", layout="wide")

st.title("📡 Monitoramento em Tempo Real - ESP32 ↔ Telegram")
st.markdown("Este painel exibe métricas de latência, temperatura e umidade registradas em tempo real.")

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
                col1.metric("Erro Médio (ME)", f"{erro_medio:.3f} s")
                col2.metric("Erro Quadrático Médio (MSE)", f"{erro_quad_medio:.3f} s²")
                col3.metric("Raiz do Erro Quadrático Médio (RMSE)", f"{raiz_erro_quad_medio:.3f} s")

                st.subheader("📈 Latência ao Longo do Tempo")
                st.line_chart(df.sort_values("timestamp_recebido")[["latencia_segundos"]])

                st.subheader("🌡 Temperatura e 💧 Umidade")
                st.line_chart(df.sort_values("timestamp_recebido")[["temperatura", "umidade"]])
        except Exception as e:
            st.warning(f"Erro ao ler CSV: {e}")
    else:
        st.info("Aguardando o arquivo de métricas...")

    time.sleep(refresh_interval)
