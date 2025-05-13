void setup() {
  pinMode(2, OUTPUT); // LED embutido no ESP32 geralmente está no pino 2
}

void loop() {
  digitalWrite(2, HIGH);
  delay(500);
  digitalWrite(2, LOW);
  delay(500);
}
