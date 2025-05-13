#include <WiFi.h>

const char* ssid = "*********";
const char* password = "*********";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Conectando");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConectado ao WiFi!");
}

void loop() {}
