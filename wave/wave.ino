#include <Servo.h>

#define SERVO_L 10
#define SERVO_R 9
#define LED_L 8
#define LED_R 7

Servo servoLeft;          // Define left servo
Servo servoRight;         // Define right servo

void setup() {
  servoLeft.attach(SERVO_L);  // Set left servo to digital pin 10
  servoRight.attach(SERVO_R);  // Set right servo to digital pin 9
  pinMode(LED_L, OUTPUT);
  pinMode(LED_R, OUTPUT);
}

void loop() {
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
