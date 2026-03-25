#include <ArduinoJson.h>

void setup() {
  Serial.begin(115200);

  pinMode(LED_BUILTIN, OUTPUT);

  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, Serial);

    if (!error) {
      String status = doc["led"];
      if (status == "on") {
        digitalWrite(LED_BUILTIN, HIGH);
      }
      if (status == "off") {
        digitalWrite(LED_BUILTIN, LOW);
      }
    }
  }
}
