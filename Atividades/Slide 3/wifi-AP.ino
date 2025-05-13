#include <WiFi.h>

const char* ssid = "ESP32-AP";
const char* password = "12345678";

void setup() {
  Serial.begin(115200);
  WiFi.softAP(ssid, password);
  Serial.println("Ponto de acesso criado");
}

void loop() {}
