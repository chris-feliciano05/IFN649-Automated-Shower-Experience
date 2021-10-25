#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 11
#define rxPin 7 // Teensy pin 7 <--> HC-05 Tx
#define txPin 8 // Teensy pin 8 <--> HC-05 Rx
OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

 float Celcius=0;
 float Fahrenheit=0;
void setup(void)
{
  Serial.begin(9600);
  Serial1.begin(9600);
  sensors.begin();
}

void loop(void)
{ 
  sensors.requestTemperatures(); 
  Celcius=sensors.getTempCByIndex(0);
  Fahrenheit=sensors.toFahrenheit(Celcius);
  Serial.print(" C  ");
  Serial.print(Celcius);
  Serial.print(" F  ");
  Serial.println(Fahrenheit);
  Serial1.print(" C  ");
  Serial1.print(Celcius);
  Serial1.print(" F  ");
  Serial1.println(Fahrenheit);
  delay(1000);
}
