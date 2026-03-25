#include <ArduinoJson.h>
#include <Servo.h>

const int servoPin = 9;

Servo myServo;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(50);

  myServo.attach(servoPin);

  myServo.write(90);
}

void loop() {
  if (Serial.available() > 0) {
    JsonDocument doc;

    DeserializationError error = deserializeJson(doc, Serial);

    if (!error) {
      int angle = doc["angle"];
      myServo.write(angle);
    }
  }
}
