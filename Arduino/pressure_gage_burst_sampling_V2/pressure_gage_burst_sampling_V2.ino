#include <Wire.h>
#include <SparkFun_MS5803_I2C.h>
#include <SD.h>
#include "RTClib.h"
#include <avr/sleep.h>
#include <avr/wdt.h>

#define ECHO_TO_SERIAL 1
#define SDPIN 8

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

int Year, Month, Day, Hour, Minute, Second; // variables to differentiate time elements
RTC_DS3231 RTC; // define the Real Time Clock object

volatile bool flag = true;
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
  Serial.begin(115200);
  sensor.reset();
  sensor.begin();
  pressure_abs = sensor.getPressure(ADC_4096);
  DateTime now=RTC.now();
  Year=now.year(); Month=now.month(); Day=now.day();
  Hour=now.hour(); Minute=now.minute(); Second=now.second();
  Serial.println();
 
  // initialize the SD card
  Serial.print("Initializing SD card...");
  // make sure that the default chip select pin is set to
  // output, even if you don't use it:
  pinMode(SDPIN, OUTPUT);
  
  // see if the card is present and can be initialized:
  if (!SD.begin(SDPIN)) {
    error("Card failed, or not present");
  }
  Serial.println("card initialized.");
  
  // create a new file
  char filename[] = "LOGGER00.CSV";
  for (uint8_t i = 0; i < 100; i++) {
    filename[6] = i/10 + '0';
    filename[7] = i%10 + '0';
    if (!SD.exists(filename)) {
      // only open a new file if it doesn't exist
      logfile = SD.open(filename, FILE_WRITE); 
      break; 
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

  sleep(6); // for 1 second
  if (++sample_count >= SAMPLE_FREQ * TIME_ACTIVE) {
    sample_count = 0;
    for (unsigned int i = 0; i < TIME_INACTIVE / 4; i++) {
      sleep(32); // for 4 seconds (works precisely only when time_inactive is a multiple of 4)
    }
  }
}

// Halt operation to save power for one of the following durations based on the chosen mode value:
// 0 for ~16ms, 1 for ~32ms, 2 for ~64ms, 3 for ~0.125s, 4 for ~0.25s, 
// 5 for ~0.5s, 6 for ~1s,   7 for ~2s,   32 for ~4s,    33 for ~8s
void sleep(uint8_t mode) {
  static byte prev = ADCSRA;
  set_sleep_mode(SLEEP_MODE_PWR_DOWN); //deepest sleep mode available
  sleep_enable();
 
  sleep_bod_disable(); //save some additional power
  noInterrupts(); // disable iterrupts during execution of the next code

  MCUSR = 0; // clear "reset" flags
  WDTCSR = bit(WDCE) | bit(WDE); // set interrupt mode and prepare to change the prescaler (time period to sleep for)
  WDTCSR = bit(WDIE) | (mode & (bit(WDP3) | bit(WDP2) | bit(WDP1) | bit(WDP0))); //set prescaler bits //bit(WDP2) | bit(WDP1);
  wdt_reset(); // reset the timer before sleeping
  interrupts(); // enable interrupts again
  sleep_cpu(); // enter the sleep mode and resume on the next line after the time period set above
  
  sleep_disable();
  ADCSRA = prev;
}

// Interrupt to run when the watchdog timer finishes a cycle. 
ISR(WDT_vect) {
  wdt_disable();
  flag = true;
}
