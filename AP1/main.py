import csv
import paho.mqtt.client as mqtt
import requests
import time
import json
import os

# === Configurações do Telegram ===
TELEGRAM_TOKEN = "7971761015:AAHrrcGHJJ3AmfrMX4RrVP7KygV5R1Ao6XI"
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# === Configuração do MQTT ===
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_TOPIC = "casa/alertas/temperatura"
MQTT_TOPIC_METRICS = "casa/metricas/esp32"

# === Arquivo para armazenar os chat_ids dos usuários ===
USER_FILE = "users.json"

# === Carregar e salvar usuários ===
def load_user_ids():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_user_ids():
    with open(USER_FILE, "w") as f:
        json.dump(list(user_ids), f)

# === Verificar novos usuários no bot ===
def check_new_users():
    global last_update_id
    response = requests.get(f"{BASE_URL}/getUpdates", params={"offset": last_update_id + 1})
    
    if response.status_code == 200:
        data = response.json()
        for result in data["result"]:
            last_update_id = result["update_id"]

            if "message" in result:
                chat_id = result["message"]["chat"]["id"]
                if chat_id not in user_ids:
                    print(f"🆕 Novo usuário registrado: {chat_id}")
                    user_ids.add(chat_id)
                    send_telegram_message("✅ Você foi registrado para receber alertas!", [chat_id])
                    save_user_ids()
    else:
        print("❌ Erro ao checar novos usuários:", response.text)

# === Enviar mensagem para todos os usuários registrados ===
def send_telegram_message(msg, recipients=None):
    if recipients is None:
        recipients = user_ids

    for uid in recipients:
        payload = {"chat_id": uid, "text": msg}
        response = requests.post(f"{BASE_URL}/sendMessage", json=payload)

        if response.status_code == 200:
            print(f"✅ Mensagem enviada a {uid}")
        else:
            print(f"❌ Erro ao enviar para {uid}: {response.text}")

# === Callback MQTT ===
def on_message(client, userdata, message):
    alert_msg = message.payload.decode()
    print(f"📩 Alerta recebido via MQTT: {alert_msg}")
    send_telegram_message(alert_msg)



# Função para salvar métricas de latência
def salvar_latencia(latencia, ts_recebido, ts_esp32_real, t, h):
    file_exists = os.path.isfile("latencia_esp32_telegram.csv")
    with open("latencia_esp32_telegram.csv", mode="a", newline="") as arquivo:
        writer = csv.writer(arquivo)
        if not file_exists:
            writer.writerow(["timestamp_esp32", "timestamp_recebido", "latencia_segundos", "temperatura", "umidade"])
        writer.writerow([ts_esp32_real, ts_recebido, latencia, t, h])


# Callback para tópico de métricas (com base no ts_esp32_real)
def on_metrics_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        dados = json.loads(payload)

        print("📦 Payload recebido:", payload)

        ts_esp32_real = dados.get("ts_esp32_real")  # Esperado em segundos (timestamp absoluto)
        t = dados.get("t")
        h = dados.get("h")

        if ts_esp32_real is not None:
            ts_recebido = time.time()  # timestamp real no Python (em segundos)
            latencia = ts_recebido - ts_esp32_real

            print(f"📊 Temperatura: {t} °C | Umidade: {h} %")
            print(f"📈 Latência end-to-end: {latencia:.3f} segundos")

            print(f"📥 Recebido às: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts_recebido))}")
            print(f"📥 Recebido às: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts_esp32_real))}")

            salvar_latencia(latencia, ts_recebido, ts_esp32_real, t, h)
        else:
            print("❌ Campo 'ts_esp32_real' ausente na métrica recebida.")

    except Exception as e:
        print(f"❌ Erro ao processar métrica MQTT: {e}")


# === Inicialização ===
user_ids = load_user_ids()
last_update_id = 0

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.message_callback_add(MQTT_TOPIC_METRICS, on_metrics_message)
client.connect(MQTT_BROKER, 1883)
client.subscribe(MQTT_TOPIC)
client.subscribe(MQTT_TOPIC_METRICS)
client.loop_start()  # <- Aqui está a mudança principal!

print("🤖 Bot iniciado. Aguardando mensagens MQTT e novos usuários...")

try:
    while True:
        check_new_users()
        time.sleep(2)
except KeyboardInterrupt:
    print("🛑 Encerrando bot...")
    client.loop_stop()
    client.disconnect()
