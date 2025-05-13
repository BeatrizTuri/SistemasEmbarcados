#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32Bluetooth"); // Nome do dispositivo Bluetooth
}

void loop() {
  if (SerialBT.available()) {
    char c = SerialBT.read();
    Serial.write(c);
  }
}
