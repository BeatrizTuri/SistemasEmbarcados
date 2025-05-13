#include <WiFi.h>

void setup() {
  Serial.begin(115200);

  // Modo AP
  WiFi.softAP("ESP32-AP", "12345678");
  Serial.println("AP iniciado");

  // Modo Station
  WiFi.begin("*******", "********");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado à rede!");
}

void loop() {}
