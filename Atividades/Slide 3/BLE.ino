#include <BLEDevice.h>
#include <BLEServer.h>

void setup() {
  BLEDevice::init("ESP32_BLE");
  BLEServer *pServer = BLEDevice::createServer();
  // Serviços e características podem ser adicionados aqui
}

void loop() {
  delay(2000);
}
