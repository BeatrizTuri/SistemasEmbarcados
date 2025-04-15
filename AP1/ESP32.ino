#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define SCREEN_WIDTH 128 // Largura do display OLED, em pixels
#define SCREEN_HEIGHT 64 // Altura do display OLED, em pixels

// Configurações WiFi
const char* ssid = "Theo";
const char* password = "britney1603";

// Configurações MQTT
const char* mqtt_server = "mqtt.eclipseprojects.io"; 
const char* mqtt_alert_topic = "casa/alertas/temperatura";

WiFiClient espClient;
PubSubClient client(espClient);

// Declaração para um display SSD1306 conectado ao I2C (pinos SDA, SCL)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

#define DHTPIN 4     
#define DHTTYPE DHT11 
DHT dht(DHTPIN, DHTTYPE);

// Limites de temperatura
const float TEMP_MIN = 21.0;
const float TEMP_MAX = 27.0;

// Variáveis para controle de publicação
unsigned long lastPublishTime = 0;
const unsigned long publishInterval = 10000; 
float lastTemp = -1; 

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("conectado");
    } else {
      Serial.print("falha, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }
  delay(2000);
  display.clearDisplay();
  display.setTextColor(WHITE);
}

void loop() {
  unsigned long currentTime = millis();
  if (currentTime - lastPublishTime >= publishInterval) {
    if (!client.connected()) {
      reconnect();
    }
    client.loop();

    // Lê temperatura e umidade do sensor DHT
    float t = dht.readTemperature();
    float h = dht.readHumidity();

    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    // Envia alertas somente quando a temperatura sair dos limites e mudar de estado
    if ((t > TEMP_MAX || t < TEMP_MIN) && t != lastTemp) {
      String alertMsg = "ALERTA: Temperatura ";
      alertMsg += (t > TEMP_MAX) ? "alta: " : "baixa: ";
      alertMsg += String(t) + " °C";

      bool success = client.publish(mqtt_alert_topic, (uint8_t*)alertMsg.c_str(), alertMsg.length());
      Serial.println(success ? "📡 Alerta MQTT publicado com sucesso!" : "⚠️ Falha ao publicar alerta MQTT");


      lastTemp = t; 
    }

    lastPublishTime = currentTime; 
  }


  display.clearDisplay();

  // Display temperatura
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print("Temperature: ");
  display.setTextSize(2);
  display.setCursor(0, 10);
  display.print(dht.readTemperature());
  display.print(" ");
  display.setTextSize(1);
  display.cp437(true);
  display.write(167);
  display.setTextSize(2);
  display.print("C");

  // Display humidade
  display.setTextSize(1);
  display.setCursor(0, 35);
  display.print("Humidity: ");
  display.setTextSize(2);
  display.setCursor(0, 45);
  display.print(dht.readHumidity());
  display.print(" %");

  display.display();
}
