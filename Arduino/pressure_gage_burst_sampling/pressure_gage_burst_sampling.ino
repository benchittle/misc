#include <Wire.h>
#include <SparkFun_MS5803_I2C.h>
#include <SD.h>
#include "RTClib.h"
#include <TimerOne.h>

#define ECHO_TO_SERIAL 0

// Set the sampling frequency of the sensor (seconds).
#define SAMPLE_FREQ 1
// Length of time that the sensor should be active vs. inactive per cycle (seconds). 
// I.E. 1020 seconds = 17 minutes active, 180 seconds = 3 minutes inactive is 
// one full cycle.
#define TIME_ACTIVE 1020
#define TIME_INACTIVE 180

// Begin class with selected address
// available addresses (selected by jumper on board) 
// default is ADDRESS_HIGH

//  ADDRESS_HIGH = 0x76
//  ADDRESS_LOW  = 0x77

MS5803 sensor(ADDRESS_HIGH);
double pressure_abs;

int Year,Month,Day,Hour,Minute,Second; // variables to differentiate time elements
RTC_PCF8523 RTC; // define the Real Time Clock object

const int chipSelect = 10; // digital pin 10 for SD cs
volatile boolean flag = true;
// Counter for toggling the sensor to be inactive.
volatile unsigned int sample_count = 0;

// the logging file
File logfile;

// This void error setup is to define the error message we'll serial print and/or relay with LED lights if things aren't right
void error(char *str)
{
  Serial.print("error: ");
  Serial.println(str);
  
  // red LED indicates error
  //digitalWrite(redLEDpin, HIGH);

  while(1);
}

void setup() {
  // Convert frequency in seconds into period in microseconds for timer.
  Timer1.initialize(1000000 / SAMPLE_FREQ); 
  Timer1.attachInterrupt( timerIsr ); // attach the service routine here
    
  Serial.begin(115200);
  sensor.reset();
  sensor.begin();
  pressure_abs = sensor.getPressure(ADC_4096);
  DateTime now=RTC.now();
  Year=now.year(); Month=now.month(); Day=now.day();
  Hour=now.hour(); Minute=now.minute(); Second=now.second();
  Serial.println();
  
  #if WAIT_TO_START
  Serial.println("Type any character to start");
  while (!Serial.available());
  #endif //WAIT_TO_START

  // initialize the SD card
  Serial.print("Initializing SD card...");
  // make sure that the default chip select pin is set to
  // output, even if you don't use it:
  pinMode(10, OUTPUT);
  
  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    error("Card failed, or not present");
  }
  Serial.println("card initialized.");
  
  // create a new file
  char filename[] = "LOGGER00.CSV";
  for (uint8_t i = 0; i < 100; i++) {
    filename[6] = i/10 + '0';
    filename[7] = i%10 + '0';
    if (! SD.exists(filename)) {
      // only open a new file if it doesn't exist
      logfile = SD.open(filename, FILE_WRITE); 
      break;  // leave the loop!
    }
  }
  
  if (! logfile) {
    error("couldnt create file");
  }
  
  Serial.print("Logging to: ");
  Serial.println(filename);

  // connect to RTC
  RTC.begin();
  Wire.begin();  
  if (!RTC.begin()) {
    logfile.println("RTC failed");
  #if ECHO_TO_SERIAL
    Serial.println("RTC failed");
  #endif  //ECHO_TO_SERIAL
  }
  logfile.println("date, time, pressure");    //++++++++++++++++++++++++ CREATING HEADERS 
  #if ECHO_TO_SERIAL
    Serial.println("date, time, pressure");
  #endif //ECHO_TO_SERIAL

}

void loop() {
  if(flag == true){
  pressure_abs = sensor.getPressure(ADC_4096);
  DateTime now=RTC.now();
  Year=now.year(); Month=now.month(); Day=now.day();
  Hour=now.hour(); Minute=now.minute(); Second=now.second();
  // print the results to the Serial Monitor:
  #if ECHO_TO_SERIAL
    Serial.print("sensor = ");
    Serial.print(pressure_abs);
    Serial.print("\t date = ");
    Serial.print(Year);
    Serial.print("/");
    Serial.print(Month);
    Serial.print("/");
    Serial.print(Day);
    Serial.print("\t time = ");
    Serial.print(Hour);
    Serial.print(":");
    Serial.print(Minute);
    Serial.print(":");
    Serial.println(Second);
  #endif //ECHO_TO_SERIAL
  
  // Write to SD card:
  logfile.print(Year); 
  logfile.print("/");
  logfile.print(Month);
  logfile.print("/");
  logfile.print(Day);
  logfile.print(", ");
  logfile.print(Hour);
  logfile.print(":");
  logfile.print(Minute);
  logfile.print(":");
  logfile.print(Second);
  logfile.print(", ");
  logfile.println(pressure_abs);
  logfile.flush();
  flag = false;
  }
}

void timerIsr() {
  // If the sensor has been active long enough, toggle it off for now.
  if (sample_count++ > SAMPLE_FREQ * TIME_ACTIVE) {
    // Attach a new interrupt to resume sampling which will run after the device 
    // has been inactive for the desired amount of time.
    Timer1.setPeriod(1000000 * TIME_INACTIVE);
    Timer1.attachInterrupt(resume);
    sample_count = 0;
  }
  flag = true;
}

void resume() {
  // Reattach the regular interrupt with the previous sampling frequency to 
  // resume sampling.
  Timer1.setPeriod(1000000 / SAMPLE_FREQ);
  Timer1.attachInterrupt(timerIsr);
}
