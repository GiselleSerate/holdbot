#include <Servo.h>

#define SERVO_L 10
#define SERVO_R 9
#define LED_L 8
#define LED_R 7

Servo servoLeft;
Servo servoRight;

int freakOut;

void setup() {
  servoLeft.attach(SERVO_L);
  servoRight.attach(SERVO_R);
  pinMode(LED_L, OUTPUT);
  pinMode(LED_R, OUTPUT);
  freakOut = '0';
  Serial.begin(9600);
}

void loop() {
  int hello = Serial.available();
  if(hello) {
    freakOut = Serial.read();
    Serial.write(freakOut);
    Serial.println();
  }

  if(freakOut == '2') {
    // Panic.
    blinkAndWave();
  }
  else if(freakOut == '1') {
    // Watch. 
    lights(HIGH);
  }
  else if(freakOut == '0') {
    // Sleep. 
    lights(LOW);
  }
}

void blinkAndWave() {
    lights(HIGH);
    forward();
    delay(200);
    lights(LOW);
    reverse();
    delay(200);
    lights(HIGH);
    delay(200);
    lights(LOW);
    delay(200);
}

void lights(int highOrLow) {
  digitalWrite(LED_L, highOrLow);
  digitalWrite(LED_R, highOrLow);
}

void forward() {
  servoLeft.write(0);
  servoRight.write(180);
}

void reverse() {
  servoLeft.write(180);
  servoRight.write(0);
}
