const int redPin = 10;
const int greenPin = 9;
const int bluePin = 11;

void setup() {
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  // Red
  setColor(255, 0, 0);
  delay(1000);

  // Green
  setColor(0, 63, 0);
  delay(1000);

  // Blue
  setColor(0, 0, 63);
  delay(1000);

  // Purple
  setColor(187, 38, 176, 50);
  delay(1000);

  // Mint
  setColor(0, 50, 50, 50);
  delay(1000);

  // LED Off
  setColor(0, 0, 0);
  delay(1000);
}

/**
 * RGB LED의 색상을 설정합니다.
 * @note Common Anode(공통 양극) RGB 모듈을 사용하므로 255에서 값을 빼서 출력합니다.
 * @param r 빨강 (0~255)
 * @param g 초록 (0~255)
 * @param b 파랑 (0~255)
*/
void setColor(int r, int g, int b) {
  analogWrite(redPin, 255 - r);
  analogWrite(greenPin, 255 - g);
  analogWrite(bluePin, 255 - b);
}

/**
 * RGB LED의 색상과 밝기를 설정합니다.
 * @note Common Anode(공통 양극) RGB 모듈을 사용하므로 255에서 값을 빼서 출력합니다.
 * @param r 빨강 (0~255)
 * @param g 초록 (0~255)
 * @param b 파랑 (0~255)
 * @param brightness 밝기 (0~100%)
*/
void setColor(int r, int g, int b, int brightness) {
  int newR = (r * brightness) / 100;
  int newG = (g * brightness) / 100;
  int newB = (b * brightness) / 100;

  analogWrite(redPin, 255 - newR);
  analogWrite(greenPin, 255 - newG);
  analogWrite(bluePin, 255 - newB);
}
