#include <WiFi.h>

const char* ssid = "ESP32-Server";
const char* password = "12345678";
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.softAP(ssid, password);
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        client.println("HTTP/1.1 200 OK");
        client.println("Content-type:text/html");
        client.println();
        client.println("<h1>ESP32 Web Server</h1>");
        break;
      }
    }
    client.stop();
  }
}
