#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "*****";
const char* password = "******";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando...");
  }

  HTTPClient http;
  http.begin("http://example.com");
  int httpCode = http.GET();

  if (httpCode > 0) {
    String payload = http.getString();
    Serial.println(payload);
  }

  http.end();
}

void loop() {}
