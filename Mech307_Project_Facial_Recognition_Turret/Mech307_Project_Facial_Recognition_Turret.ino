#include <Servo.h> //Import servo library
#include <Stepper.h> //Import stepper motor library

const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution
const int oneDeg = stepsPerRevolution / 360 + 1; //converts steps per revolution into degrees per revolution

const int in[] = {10, 11, 12, 13}; // Define stepper motor in-pins
const int servopin[] = {9, 6}; // Define servomotor pins
const int buzzerPin = 3; // Define the buzzer pin
const int ledPin = 5; // Define the LED pin

const int buttonPin = A5; // Define button pin

bool fired = LOW; // tells the arduino if the gun has been fired or not

int step1;
int serv1;

Servo servo1;  // create servo object to control servo1
Servo servo2; // create servo object to control servo2
Stepper stepper(stepsPerRevolution, in[0], in[2], in[1], in[3]); // create stepper object to control stepper motor

int parsePos1; //initialize parsePos variable - used to distinguish between x and y position data
int parsePos2; //initialize parsePos variable - used to distinguish between x and y position data

void setup()
{
  servo1.attach(servopin[0]);  // attaches the servo on the first pin in the servopin array to the servo object
  servo2.attach(servopin[1]);  // attaches the servo on the first pin in the servopin array to the servo object
  servo1.write(135); // sets servo1 initial position to 45 degrees
  servo2.write(0); // sets servo0 initial position to 0 degrees
  stepper.setSpeed(10); // max motor speed is 15 rpm
  Serial.begin(19200); // initalize serial communication
}

void loop() {
  if (fired == HIGH) {
    stateFired(); //run code for when the gun is in the "fired" state
  }
  else if (Serial.available()) {
    String str = "";
    while (Serial.available()) {
      str += ((char) Serial.read());
      delay(2);
    }
    if (str != "") {
      parsePos1 = str.indexOf(" ");
      parsePos2 = str.indexOf(" ", parsePos1 + 1);
      step1 = int(str.substring(0, parsePos1).toInt());
      if (abs(step1) > 5) { // tolerance for turning turret base
        stepper.step(map(step1, -50, 50, -10, 10)*oneDeg); // map input to +/- 10 degrees
      }
      serv1=str.substring(parsePos1 + 1, parsePos2).toInt();
      servo1.write(map(serv1, 0, 100, 180, 90));
      if (str.substring(parsePos2 + 1, str.length()).toInt() >= 100) {
        servo2.write(90);
        analogWrite(buzzerPin, 255);
        delay(150);
        analogWrite(buzzerPin, LOW);
        fired = HIGH;
      }
      //delay(100);

    }
  }
  else {
  }
}

void stateFired() {
  analogWrite(ledPin, 255);
  delay(100);
  analogWrite(ledPin, LOW);
  for (int i = 1; i < 300 ; i++) {
    delay(10);
    if (analogRead(buttonPin) >= 1000) {
      fired = LOW;
      analogWrite(ledPin, LOW);
      servo2.write(0);
      i = 301;
      while(Serial.available()){Serial.read();};
    }
  }
}
