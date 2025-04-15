import paho.mqtt.client as mqtt
import requests
import time
import json
import os

# === Configurações do Telegram ===
TELEGRAM_TOKEN = ""
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# === Configuração do MQTT ===
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_TOPIC = "casa/alertas/temperatura"

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

# === Inicialização ===
user_ids = load_user_ids()
last_update_id = 0

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(MQTT_BROKER, 1883)
client.subscribe(MQTT_TOPIC)

print("🤖 Bot iniciado. Aguardando mensagens MQTT e novos usuários...")

# === Loop principal ===
while True:
    check_new_users()
    client.loop(timeout=1.0)
    time.sleep(2)
