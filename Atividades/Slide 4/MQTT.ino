#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "********";
const char* password = "********";
const char* mqtt_server = "test.mosquitto.org";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;

void setup_wifi() {
  delay(10);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi conectado!");
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32Client")) {
      Serial.println("Conectado ao broker MQTT");
    } else {
      delay(5000);
    }
  }
}

void setup() {
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 10000) {
    lastMsg = now;

    int fakeSensor = analogRead(34); // exemplo de leitura
    char msg[50];
    snprintf(msg, 50, "Sensor: %d", fakeSensor);

    Serial.print("Publicando: ");
    Serial.println(msg);
    client.publish("iotbr/esp32", msg);
  }
}
