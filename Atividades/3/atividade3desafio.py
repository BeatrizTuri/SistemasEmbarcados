import network
import time
from umqtt.simple import MQTTClient

SSID = "Serejo"
PASSWORD = "Serejolas"

BROKER = "test.mosquitto.org"
TOPIC = "iotbr/esp32"

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(SSID, PASSWORD)

while not sta_if.isconnected():
    time.sleep(1)

print("Conectado ao Wi-Fi")

client = MQTTClient("esp32", BROKER)
client.connect()

while True:
    sensor_value = 25.0 
    client.publish(TOPIC, f"Temperatura: {sensor_value}°C")
    print(f"Publicado: Temperatura: {sensor_value}°C")
    time.sleep(10)
""