void setup() {
  Serial.begin(115200);

  pinMode(LED_BUILTIN, OUTPUT);

  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();

    if (cmd == '1') {
      digitalWrite(LED_BUILTIN, HIGH);
    } else if (cmd == '0') {
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}
