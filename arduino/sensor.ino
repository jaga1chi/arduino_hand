#include<Wire.h>
const int MPU_ADDR = 0x68;    // I2C통신을 위한 MPU6050의 주소
const int FLEX_RC_PIN = 2;  // D2

int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;   // 가속도(Acceleration) 와 

int flexpin1 = A0;
int flexpin2 = A1;
int flexpin3 = A2;
int flexpin4 = A3;

void getRawData();  // 센서값 얻는 서브함수의 프로토타입 선언 

unsigned long readFlexRC(int pin) {
  // 1) 완전 방전
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
  delay(5); // 5ms 정도 확실히 방전

  // 2) 입력으로 전환 후 충전 시간 측정
  unsigned long t0 = micros();
  pinMode(pin, INPUT);  
  // LOW에서 HIGH로 넘어갈 때까지 대기
  while (digitalRead(pin) == LOW) {
    if (micros() - t0 > 300000UL) { // 300ms 타임아웃
      return 300000UL; // 너무 오래 걸리면 이 값 반환
    }
  }
  return micros() - t0; // μs 단위 시간 (클수록 더 많이 굽힘)
}

void setup() {
  initSensor();
  Serial.begin(9600);
}

void loop() {
  unsigned long t = readFlexRC(FLEX_RC_PIN);
  int flexVal;
  int flexVal1;
  int flexVal2;
  int flexVal3;

  flexVal = analogRead(flexpin1);
  flexVal1 = analogRead(flexpin2);
  flexVal2 = analogRead(flexpin3);
  flexVal3 = analogRead(flexpin4);

  Serial.print(480-t/28); //digital pin값 정규화
  Serial.print(",");
  Serial.print(flexVal);
  Serial.print(",");
  Serial.print(flexVal1);
  Serial.print(",");
  Serial.print(flexVal2);
  Serial.print(",");
  Serial.print(flexVal3);
  Serial.print(",");

  getRawData(); 
  Serial.print(AcX);
  Serial.print(",");
  Serial.print(AcY);
  Serial.print(",");
  Serial.print(AcZ);
  Serial.print(",");
  Serial.print(GyX);
  Serial.print(",");
  Serial.print(GyY);
  Serial.print(",");
  Serial.print(GyZ);
  Serial.println();
}
void initSensor() {
  Wire.begin();
  Wire.beginTransmission(MPU_ADDR);   // I2C 통신용 어드레스(주소)
  Wire.write(0x6B);    // MPU6050과 통신을 시작하기 위해서는 0x6B번지에    
  Wire.write(0);       // MPU6050을 동작 대기 모드로 변경
  Wire.endTransmission(true);
}
void getRawData() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);   // AcX 레지스터 위치(주소)를 지칭합니다
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 14, true);  // AcX 주소 이후의 14byte의 데이터를 요청

  AcX = Wire.read() << 8 | Wire.read(); //두 개의 나뉘어진 바이트를 하나로 이어 붙여서 각 변수에 저장
  AcY = Wire.read() << 8 | Wire.read();
  AcZ = Wire.read() << 8 | Wire.read();
  Tmp = Wire.read() << 8 | Wire.read();
  GyX = Wire.read() << 8 | Wire.read();
  GyY = Wire.read() << 8 | Wire.read();
  GyZ = Wire.read() << 8 | Wire.read();
}
