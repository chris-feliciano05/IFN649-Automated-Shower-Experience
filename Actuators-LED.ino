
#define rxPin 8  Teensy pin 7 -- HC-05 Tx
#define txPin 7  Teensy pin 8 -- HC-05 Rx
#define LEDPIN 11

const int redPin = 14;
const int yellowPin = 12;
const int greenPin = 10;
//const int sensorPin = A0;
String command;


void setup() {

Serial.begin(9600);

//Setup Serial1 for BlueTooth
Serial1.begin(9600);  //Default communication rate of the Bluetooth module

pinMode(redPin, OUTPUT);
pinMode(yellowPin, OUTPUT);
pinMode(greenPin, OUTPUT);


}
void loop() {

    command = Serial1.readStringUntil('n');
    command.trim();
    Serial.println(command);
    if(command.equals("High")){
      digitalWrite(redPin, HIGH);
      digitalWrite(yellowPin, LOW);
      digitalWrite(greenPin, LOW);
    }
    else if(command.equals("Medium")){
      digitalWrite(redPin, LOW);
      digitalWrite(yellowPin, HIGH);
      digitalWrite(greenPin, LOW);
     
    }
    else if(command.equals("Low")){
      digitalWrite(redPin, LOW);
      digitalWrite(yellowPin, LOW);
      digitalWrite(greenPin, HIGH);
    }
    else if(command.equals('No Value')){
      digitalWrite(redPin, LOW);
      digitalWrite(yellowPin, LOW);
      digitalWrite(greenPin, LOW);
    }
   
}
