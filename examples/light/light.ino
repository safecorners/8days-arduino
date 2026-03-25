#include <ArduinoJson.h>

const int lightSensorPin = A0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int lightValue = analogRead(lightSensorPin);
  
  JsonDocument doc;
  doc["type"] = "light";
  doc["value"] = lightValue;

  serializeJson(doc, Serial);
  Serial.println();

  delay(500);
}