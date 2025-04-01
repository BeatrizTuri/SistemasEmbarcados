import paho.mqtt.client as mqtt
import requests

# Configurações do Telegram
TELEGRAM_TOKEN = "7971761015:AAHrrcGHJJ3AmfrMX4RrVP7KygV5R1Ao6XI"
CHAT_ID = "7525968418"

# Configuração do MQTT
MQTT_BROKER = "broker.mqtt-dashboard.com"
MQTT_TOPIC = "casa/alertas/temperatura"

# Função para enviar mensagem ao Telegram
def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("✅ Mensagem enviada ao Telegram!")
    else:
        print(f"❌ Erro ao enviar mensagem: {response.text}")

# Callback chamado quando uma mensagem MQTT é recebida
def on_message(client, userdata, message):
    alert_msg = message.payload.decode()
    print(f"📩 Alerta recebido via MQTT: {alert_msg}")
    send_telegram_message(alert_msg)

# Configuração do cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(MQTT_BROKER, 1883)
client.subscribe(MQTT_TOPIC)

print("📡 Aguardando mensagens MQTT...")

client.loop_forever()
