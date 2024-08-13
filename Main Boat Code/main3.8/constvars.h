//This file for constant variables or parameters used across multiple areas of the code or for configuration purposes

#include "pindefinitions.h"
#include <SoftwareSerial.h>
#include <TinyGPSPlus.h>
#include <Adafruit_LIS2MDL.h>
#include <Adafruit_INA260.h>
#include <ping1d.h>

#ifndef CONST_VARS_h
#define CONST_VARS_h



const float Pi = 3.15159;


//SD card stuff
File coords;
File blackbox;
File depthlog;
File errorlog;
int bblast = 0;       //millis() of previous black box recording
int bbint = 1;       //seconds between black box recordings
int depthlast = 0;      //millis() of previous depth recording
int depthint = 30;      //seconds between depth measurements
bool cardfailed;
char cardcontents[25];
int cardsize;
byte i = 0;           //indexes for nested loops that read coordinate arrays
byte j = 0;
byte k = 1;
byte n;
const byte maxcoords = 25;    //maximum allowable number of gps coordinate pairs in mission. Helps save RAM

//GPS and auto navigation stuff
TinyGPSPlus gps;
float currentLat;
float currentLong;
float goalLat = 39.03385;
float goalLong = 125.75432;
float Carray [2][maxcoords];        //array of latitude and longitude pairs (row 0 lat row 1 long, column 0 only contains the length)
byte ncoords = maxcoords;                         //number of coordinate pairs
double goalheading;
double hdiff;                   //difference between actual heading and goal heading
double hdarr[5] = {0};          //array of the last 5 hdiff values
double hdsum = 0;
double hdavg = 0;               //average of the last 5 hdiff values. This intended to smooth out jumpy magnetometer data.
byte waypoint = 1;
double d = 100;
bool killhumansmode = false;

//Drive control stuff
Servo port;
Servo starboard;
Servo rudder;
int portval;        // actual pwm values in microseconds to feed ESCs
int starbval;
int rudval;
int goalport;       //goal pwm values for gradual adjustment
int goalstarb;    
int goalrud;
int switchval = 0;  //1 switch flipped 0 switch not flipped. 1 is manual control mode.
bool autostate = true;
int throtval = 0;   //throttle value. zero is dead stop, -100 is full power backwards, 100 is full power forwards
int steerval = 0;   //steering value. -100 is hard left, positive 100 is hard right, zero straight 
const float pwmhigh = 2000;   //pwm range values for installed ESCs. virtually always 1000-2000 for typical RC or drone parts. 
const float pwmmid = 1500;    //pwm midpoint for ESC neutral/startup
const float pwmlow = 1000;
const float servlow = 500;       //min, middle, max signals for full range of rudder servo
const float servmid = 1500;
const float servhigh = 2500;
const int pwmim = 100;         //milliseconds between each pwm adjustment for motor ESCs
const int pwmir = 100;          //milliseconds between each pwm adjustment for rudder servo; (NOTE: Rudder incremental adjustment not currenlty implemented)
const int pwmratem = 25;      //maximum allowed microseconds of pwm adjustment for motor ESCs per pwmim miliseconds. for example, a value of 1 and i of 10 would take 10 seconds to go from a pwm of 1000us to 2000us. a value of 5 would take 2 seconds.
const int pwmrater = 100;     //maximum allowed microseconds of pwm adjustment for rudder servo per pwmir miliseconds. for example, a value of 1 and i of 5 would take 10 seconds to go from a pwm of 500us to 2500us. a value of 5 would take 2 seconds.
unsigned long tlastp = 0;     //time in ms since last pwm adjustment
unsigned long tlasts = 0;
unsigned long tlastr = 0;

//PID Control
const float Kp = 1;       //proportional gain
const float Ki = .125;    //integral gain
const float Kd = 0;       //derivative gain
float Setpoint, PIDInput, PIDOutput;
QuickPID steerPID(&PIDInput, &PIDOutput, &Setpoint);


//Magnetometer stuff
Adafruit_LIS2MDL mag = Adafruit_LIS2MDL(12345); 
bool magerr;
float currentheading;
const float xoff = -19.87;        //from magnetometer calibration
const float yoff = -21.22;
const float declination = 3.1;    //from central texas 2024

//Power measurement stuff (INA260)
Adafruit_INA260 motpow = Adafruit_INA260(); //motor and whole system power consumption
Adafruit_INA260 solpow = Adafruit_INA260(); //solar power production
double motI = 0;  //mA
double solI = 0;
double motV = 0;  //mV
double solV = 0;
const double motIlimit = 20000; //mA at which forced throttle down should occur

//depth sounder stuff
Ping1D ping { Serial2 };
int depth = 0;

//error code stuff
int laste2 = 0;
int laste3 = 0;
int laste6 = 0;
int laste7 = 0;
int lastgoodhead = 0;

//for checking speed that program runs
unsigned long loopt = 0;
unsigned long looptlast = 0;

#endif
