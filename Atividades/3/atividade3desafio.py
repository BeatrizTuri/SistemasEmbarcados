import paho.mqtt.client as mqtt
import time
import random

# Configurações do Broker
broker = "test.mosquitto.org"
topic = "iotbr/esp32"

# Conectar ao Broker
client = mqtt.Client()
client.connect(broker, 1883, 60)

try:
    while True:
        temperatura = round(random.uniform(20.0, 30.0), 2)  # Simula uma temperatura entre 20 e 30°C
        mensagem = f"Temperatura: {temperatura}°C"
        client.publish(topic, mensagem)
        print(f"Publicado: {mensagem}")
        time.sleep(10)  # Espera 10 segundos antes de enviar novamente
except KeyboardInterrupt:
    print("Finalizando...")
    client.disconnect()
