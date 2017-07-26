// This code originates from the MagnusFlieger/Arduino respository
// which can be found here: https://github.com/MagnusFlieger/Arduino/

#include <Servo.h>
Servo myservo;  // create servo object to control a servo

int pos = 90;    // variable to store the servo position
int Change = 0;

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  myservo.write(pos);
}

void loop() {
  int Read = Serial.read();
  // When Serial.read() equals -1, then no data has been transferred
  if (Read != -1) {
    Serial.print(Read);
    myservo.write(Read);
  }
  delay(100);
}
