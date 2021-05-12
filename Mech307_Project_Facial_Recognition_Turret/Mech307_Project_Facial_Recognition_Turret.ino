#include <Servo.h> //Import servo library
#include <Stepper.h> //Import stepper motor library

const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution
const int oneDeg = stepsPerRevolution / 360 + 1; //converts steps per revolution into degrees per revolution

const int in[] = {10, 11, 12, 13}; // Define stepper motor in-pins
const int servopin[] = {9, 6}; // Define servomotor pins
const int buzzerPin = 3; // Define the buzzer pin
const int ledPin = 5; // Define the LED pin

const int buttonPin = A5; // Define button pin

bool fired = HIGH; // tells the arduino if the gun has been fired or not

int step1; //initialize step variable
int serv1; //initialize serv1 variable
int fireInput; //initialize fireInput variable

Servo servo1;  // create servo object to control servo1
Servo servo2; // create servo object to control servo2
Stepper stepper(stepsPerRevolution, in[0], in[2], in[1], in[3]); // create stepper object to control stepper motor

int parsePos1; //initialize parsePos variable - used to distinguish between x and y position data
int parsePos2; //initialize parsePos variable - used to distinguish between x and y position data

void setup()
{
  servo1.attach(servopin[0]);  // attaches the servo on the first pin in the servopin array to the servo object
  servo2.attach(servopin[1]);  // attaches the servo on the first pin in the servopin array to the servo object
  servo1.write(135); // sets servo1 initial position to 135 degrees
  servo2.write(0); // sets servo0 initial position to 0 degrees
  stepper.setSpeed(10); // max motor speed is 15 rpm
  Serial.begin(19200); // initalize serial communication
}

void loop() {
  if (fired == HIGH) { //check if gun is has been fired
    stateFired(); //run code for when the gun is in the "fired" state
  }
  else if (Serial.available()) { //check for serial input
    String str = ""; //Create empty string
    while (Serial.available()) { //read serial input
      str += ((char) Serial.read()); //store serial input as a string
      delay(2); //wait for next character to be read
    }
    if (str != "") { //check if string is empty
      parsePos1 = str.indexOf(" "); //find first space in string; store to parsePos1
      parsePos2 = str.indexOf(" ", parsePos1 + 1); //find second space in string; store to parsePos2
      step1 = int(str.substring(0, parsePos1).toInt()); //read first number; store to step1
      serv1 = str.substring(parsePos1 + 1, parsePos2).toInt(); // read second number; store to serv1
      fireInput = str.substring(parsePos2 + 1, str.length()).toInt(); //read third number; store to fireInput
      if (abs(step1) > 4) { // tolerance for turning turret base
        stepper.step(map(step1, -50, 50, -10, 10)*oneDeg / 2); // map input to +/- 10 degrees and rotate stepper
      }
      servo1.write(map(serv1, 0, 100, 170, 120)); //map input to 170-120 degrees and rotate servo motor
      if (fireInput > 0) { //check if fireInput is > 0
        analogWrite(ledPin, fireInput * 255 / 100); //Change led brightness to match fireInput
      }
      else { 
        analogWrite(ledPin, 0); //Turn off led
      }
      if (fireInput >= 100) { //check if fireInput is greater than 100
        analogWrite(ledPin, 0); //turn off led
        servo2.write(180); //pull trigger with servo 2
        analogWrite(buzzerPin, 255); //turn on buzzer
        delay(150);
        analogWrite(buzzerPin, LOW); // turn off buzzer
        delay(500);
        servo2.write(0); // release trigger
        fired = HIGH; //change fired state to true
      }
    }
  }
}

void stateFired() {
  //blink led
  analogWrite(ledPin, 255);
  delay(100);
  analogWrite(ledPin, LOW);
  // wait for button press
  for (int i = 1; i < 300 ; i++) {
    delay(10);
    if (analogRead(buttonPin) >= 1000) {//check for button press
      fired = LOW; // reset fire state to false
      analogWrite(ledPin, LOW); //turn off led
      servo2.write(0); //release trigger
      i = 301; //exit for loop
      while (Serial.available()) { //check if serial data is available
        Serial.read(); //clear serial buffer
      };
    }
  }
}
