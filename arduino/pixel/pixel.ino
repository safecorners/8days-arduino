#include <Adafruit_NeoPixel.h>

const int neoPin = 6;
const int numberOfLed = 4;
/*
  * 네오픽셀 객체를 생성합니다.
  * @param numberOfLed LED의 개수
  * @param neoPixelPin 네오픽셀의 데이터 핀 번호
  * @param NEO_GRB + NEO_KHZ800 네오픽셀의 색상 순서와 통신 속도
*/
Adafruit_NeoPixel pixels(numberOfLed, neoPin, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin();
  pixels.setBrightness(50);
  pixels.clear();

  Serial.begin(115200);
}

/*
 * 네오픽셀의 색상을 설정합니다.
 * @param r 빨강 (0~255)
 * @param g 초록 (0~255)
 * @param b 파랑 (0~255)
*/
void setColor(int r, int g, int b) {
  pixels.clear();

  pixels.fill(
    pixels.Color(r, g, b),
    0,
    numberOfLed
  );

  pixels.show();
}

void loop() {
  setColor(255, 0, 0);
  delay(1000);
  
  setColor(0, 255, 0);
  delay(1000);

  setColor(0, 0, 255);
  delay(1000);
}
