//Clay M
//Updated 4-19-2025

//GUMPTION TRAP II MAIN CODE
//This code written for custom PCB v1.2
//First version with newly rebuilt boat, Gumption Trap II. New hardware includes bidirectional ESCs and a rudder servo
//Designed to run on Gumption Trap II, a solar powered USV with two bidirectional brushless motors and a servo driven rudder system.
//Hardware also includes a GPS module, Magnetometer, Blue Robotics Ping Echo Sounder, two INA260 Current/Voltage Sensors and an SD card module.
//Main microcontroller is a PJRC Teensy 4.0

//Local Backup Version 3.11

//Changes from previous public upload (local backup 3.8):
/*
  -Improve PID tuning
  -now print serial debugging values only if USB plugged into laptop. Will run faster when unplugged this way.
  -other minor changes to make code run faster
*/

//Test Results: 
/*
  -Worked flawlessly in real world lake test. (4.12.25). Made sharp turns nicely without overshooting. 
  -Power consumption/generation was about 1:1 on a sunny day.
*/

#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>
#include <SD.h>
#include <SPI.h>
#include <Adafruit_LIS2MDL.h>       
#include <Servo.h>
#include <Adafruit_INA260.h>
#include <ping1d.h>
#include <QuickPID.h>

#include "pindefinitions.h"
#include "miscfuncs.h"
#include "constvars.h"
#include "manualmode.h"
#include "automode.h"
#include "powersense.h"
#include "cardlogger.h"
#include "depthping.h"
#include "navigation.h"




void setup() 
{
  Serial.begin(115200);
  
  //make sure SD card is good
  if(!SD.begin(cs))
  {
    cardfailed = true;
    Serial.println("couldn't initialize");
  }
  else
  {
    cardfailed = false;
    Serial.println("SD Card Initialized");
  }

  if(!SD.exists("COORDS.txt"))
  {
    cardfailed = true;
    Serial.println("File Missing");
  }

  //pull coords off SD Card
  if(!cardfailed)
  {
    readcard();
    printCoords();
  }
  else
  {
    Serial.println(F("Card read failed"));
  }

  //check for magnetometer error
  if(!mag.begin())              
  {
    magerr = true;
    Serial.println("MAG ERROR");
    logerror(4);
  } 
  
  //setup ping sounder 
  Serial2.begin(115200);
  if(!ping.initialize())
  {
    Serial.println("PING ERROR");
    logerror(5);
  }
  
  //initialize gps serial connection
  Serial1.begin(9600);
  
  //drive control setup
  pinMode(throt, INPUT);
  pinMode(steer, INPUT);
  pinMode(swt, INPUT);

  //initialize motors
  port.attach(pmot,pwmlow,pwmhigh);
  starboard.attach(smot,pwmlow,pwmhigh);
  rudder.attach(rud,servlow,servhigh);

  port.write(pwmmid);          //set throttles to neutral to make sure ESC's will start up.
  starboard.write(pwmmid);
  rudder.write(servmid);
  portval = pwmmid;
  starbval = pwmmid;
  rudval = servmid;
  
  //setup power measurement chips (INA260)
  motpow.begin(0x41);   //note: one module needs a solder jumper so that they have different I2C addresses
  solpow.begin(0x40);
  
  //setup PID Control loop
  Setpoint = 0;
  steerPID.SetTunings(Kp, Ki, Kd);
  steerPID.SetOutputLimits(-100,100);
  steerPID.SetMode(0); //start in manual mode
  
  smartDelay(5000); //take some time to read gps data
  Serial.println("setup over");
}

void loop() 
{
  switchval = readSwitch(swt, false);  //check the mode toggle switch. if out of radio range, default to auto
  powersense();
  depthping();
  if(Serial)          //if usb is plugged in, print the debugging values
    {printvals();}
  blackboxwrite();
  pingwrite();
  navigate();
  steerPID.Compute();
  looptimecheck();
  
  if(!switchval)  //this extra if statement is a little redundant, included because I had plans for some other ways autostate might be enabled or disabled besides just switchval.
    {autostate = true;}
  else    
    {autostate = false;}  
    
  if(autostate)    
    {
      steerPID.SetMode(1); //automatic mode
      automode();
    }
  else
    {
      steerPID.SetMode(0); //manual mode
      manualmode();
    } 
}
