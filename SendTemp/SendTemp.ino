#include<SPI.h>
#include<RF24.h>
#include <DallasTemperature.h>

#include <OneWire.h>
#include <DallasTemperature.h>
// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 2
// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);

RF24 radio(9, 10);
//Sound
int micPin = A1;
//Light
int LDR = 0;
int LDRValue = 0;
int micValue = 0;

char SendPayload[15] = "";
char char_array[5] = "";
char char_array2[5] = "";
char char_array3[5]= "";
 
void setup(void)
{
  Serial.begin(57600); //Debug 
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.powerUp();
}


void loop(void)
{
    float temp = 0;
    sensors.requestTemperatures();
    temp = sensors.getTempCByIndex(0);
    LDRValue = analogRead(0);
    micValue = analogRead(1);

  // Send the command to get temperatures
  Serial.println("Light value:");
  Serial.println(LDRValue);
  Serial.println("Sound Value:");
  Serial.println(micValue);

  String tempValue = "C";
  tempValue  += temp; 

  // Define 
  String lightValue = "L";
  lightValue  += LDRValue;
  
  String soudvalue = "S";
  soudvalue += micValue;
  
  // Copy it over 
  lightValue.toCharArray(char_array, 5);
  soudvalue.toCharArray(char_array2, 5);
  tempValue.toCharArray(char_array3, 5);

  strcat(SendPayload,char_array);
  strcat(SendPayload,char_array2);
  strcat(SendPayload,char_array3);

 // String myString = String(int (sensors.getTempCByIndex(0)));
  radio.write(&SendPayload,strlen(SendPayload));
  delay(100);
}
