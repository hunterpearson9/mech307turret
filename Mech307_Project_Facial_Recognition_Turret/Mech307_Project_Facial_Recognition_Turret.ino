#include <Servo.h> //Import servo library
#include <Stepper.h> //Import stepper motor library

const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution
const int oneDeg = stepsPerRevolution / 360 + 1; //converts steps per revolution into degrees per revolution

const int in[] = {2, 3, 4, 5}; // Define stepper motor in-pins
const int servopin[] = {10}; // Define servomotor pins
const int buzzerPin = 11; // Define the buzzer pin

bool fired = LOW; // tells the arduino if the gun has been fired or not

Servo servo1;  // create servo object to control servo1
Stepper stepper(stepsPerRevolution, in[0], in[2], in[1], in[3]); // create stepper object to control stepper motor

int parsePos; //initialize parsePos variable - used to distinguish between x and y position data

void setup()
{
  servo1.attach(servopin[0]);  // attaches the servo on the first pin in the servopin array to the servo object
  servo1.write(45); // sets servo1 initial position to 45 degrees
  stepper.setSpeed(15); // sets stepper motor speed to 15 rpm
  Serial.begin(9600); // initalize serial communication
}

void loop() {
  if (Serial.available()) {
    String str = "";
    while (Serial.available()) {
      str += ((char) Serial.read());
      delay(2);
    }
    if (str != "") {
      parsePos = str.indexOf(" ");
      Serial.println(str.substring(parsePos + 1, str.length()).toInt());
      stepper.step(int(str.substring(0, parsePos).toInt()*oneDeg));
      servo1.write(str.substring(parsePos + 1, str.length()).toInt()); // tell servo to go to position in variable 'pos'
      delay(100);

    }
  }
  else {
    if (fired == HIGH) {
      soundFired(); //activate buzzer
    }
  }
}

void soundFired() {
  analogWrite(buzzerPin, 1);
  delay(100);
  analogWrite(buzzerPin, LOW);
  for (int i = 1; i >= 29 ; i++) {
    delay(100);
    if (fired == LOW) {
      i = 30;
    }
  }
}
