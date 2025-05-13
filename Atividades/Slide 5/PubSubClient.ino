#include <WiFi.h>
#include <PubSubClient.h>

// Credenciais Wi-Fi
const char* ssid = "*********";
const char* password = "*********";

// Dados do broker
const char* mqtt_server = "test.mosquitto.org";
const int mqtt_port = 1883; // sem TLS
const char* mqtt_user = ""; // vazio, broker não exige
const char* mqtt_password = "";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;

void setup_wifi() {
  delay(10);
  Serial.begin(115200);
  Serial.println();
  Serial.print("Conectando-se ao WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado!");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando ao broker MQTT...");
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("conectado!");
    } else {
      Serial.print("falhou. Código = ");
      Serial.print(client.state());
      delay(5000);
    }
  }
}

void setup() {
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 10000) { // a cada 10 segundos
    lastMsg = now;

    int leituraSensor = analogRead(34); // ou qualquer pino que queira simular
    char mensagem[50];
    snprintf(mensagem, 50, "Leitura: %d", leituraSensor);

    Serial.print("Publicando mensagem: ");
    Serial.println(mensagem);

    client.publish("iotbr/esp32", mensagem);
  }
}
