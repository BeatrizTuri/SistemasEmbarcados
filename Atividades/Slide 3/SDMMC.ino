#include "FS.h"
#include "SD_MMC.h"

void setup() {
  Serial.begin(115200);
  if (!SD_MMC.begin()) {
    Serial.println("Falha ao montar SD_MMC");
    return;
  }

  File file = SD_MMC.open("/teste.txt", FILE_WRITE);
  if (file) {
    file.println("Olá, cartão SD!");
    file.close();
    Serial.println("Arquivo escrito!");
  } else {
    Serial.println("Erro ao abrir o arquivo");
  }
}

void loop() {}
