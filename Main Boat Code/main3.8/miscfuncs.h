//miscellanous functions used for multiple things
#include "constvars.h"

#ifndef MISC_FUNCS_h
#define MISC_FUNCS_h

//this function is for gradually ramping pwm up and down to limit the rate of motor acceleration. p is desired PWM rate, m is motor select (0 for port 1 for stbd)
void adjustpwm(int p, int m)
{
  int p0;   //current actual pwm
  unsigned long t0;   //time of last adjustment
  int p1; //output pwm that will be written to esc
  int pwmrate;
  int pwmi;
  
  //pull variables for the correct motor
  if(m == 1)
  {
    p0 = starbval;
    t0 = tlasts;
    pwmrate = pwmratem;
    pwmi = pwmim;
  }
  else if(m == 0) 
  {
    p0 = portval;
    t0 = tlastp;
    pwmrate = pwmratem;
    pwmi = pwmim;
  }
  else if(m == 2)
  {
    p0 = rudval;
    t0 = tlastr;
    pwmrate = pwmrater;
    pwmi = pwmir;
  }
  else
  {return;}
  
  //stop and do nothing if not enough time has passed since last adjustment
  if((millis()-t0)<pwmi)
  {return;}
  
  //set pwm directly to goal if its within a step
  if(abs(p0-p)<=pwmrate)
  {p1 = p;  }
  
  else if(p0>p) //if actual is higher than goal, reduce it a step
  {p1 = p0-pwmrate;}
  
  else if(p0<p) //if actual is lower than goal, add by a step
  {p1 = p0+pwmrate;}
  
  if(m == 1)
  {
    starboard.writeMicroseconds(p1);
    starbval = p1;
    tlasts = millis();
  }
  else if(m == 0)
  {
    port.writeMicroseconds(p1);
    portval = p1;
    tlastp = millis();
  }
  else
  {
    /*rudder.writeMicroseconds(p1);
    rudval = p1;
    tlastr = millis();*/
    
    //rudder functionality currently commented out, partially tested but the code runs too slowly to smoothly adjust rudder position so I'm leaving it discrete for now
  }
}

//for delaying while still reading gps coords
static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (Serial1.available())
      gps.encode(Serial1.read());
  } while (millis() - start < ms);
}

//pulls the coordinates off of the SD card
static void readcard()
{ 
  coords = SD.open("COORDS.txt", FILE_READ);
  while(j<(ncoords+1))      //while theres still data to be read
  {
    char aChar = coords.read();           //read all the data, put them into a char array
    if(aChar != '\n' && aChar != '\r')
    {
      cardcontents[i++] = aChar;
      cardcontents[i] = '\0'; 
    }
    else
    {
      if(strlen(cardcontents) > 0)
      {
        float Val = atof(cardcontents);     //convert data into floats

        Carray[k][j] = Val;       
        if(k==1)
        {j++;}
        k++;
        if(k > 1)       //alternate every other one to switch between latitude/longitude
        {k-=2;}

        if(j<2)
        {
          ncoords = Carray[1][0];     //the first number in the file is the number of coordinate pairs. 
        }
      }
      cardcontents[0] = '\0';
      i = 0;
    }
  }
  coords.close(); 
}

//This is to read a pwm radio channel
int readChannel(int inpin, int minlim, int maxlim, int defaultval)
{
  int val = pulseIn(inpin, HIGH, 30000);
  if(val<100)
    {return defaultval;}  
  return map(val, 1000,2000,minlim,maxlim);
}
//This one reads a switch
bool readSwitch(byte switchin, bool defaultval)
{
  int dval = (defaultval)? 100: 0;
  int out = readChannel(switchin, 0,100, dval);       
  return (out>50);                               
}

//prints key variables over serial for debugging. 
void printvals()
{
  Serial.print("     port: ");
  Serial.print(portval);
  Serial.print("     starb: ");
  Serial.print(starbval);
  Serial.print("     rudd: ");
  Serial.print(rudval);
  Serial.print("     goalport: ");
  Serial.print(goalport);
  Serial.print("     goalstarb: ");
  Serial.print(goalstarb);
  Serial.print("     goalrud: ");
  Serial.print(goalrud);
  Serial.print("     throt: ");
  Serial.print(throtval);
  Serial.print("     steer: ");
  Serial.print(steerval);
  Serial.print("     motI: ");
  Serial.print(motI);
  Serial.print("     solI: ");
  Serial.print(solI);
  Serial.print("     motV: ");
  Serial.print(motV);
  Serial.print("     solV: ");
  Serial.print(solV);
  Serial.print("     Lat: ");
  Serial.print(currentLat,6);
  Serial.print("     Long: ");
  Serial.print(currentLong,6);
  Serial.print("     Head: ");
  Serial.print(currentheading);
  Serial.print("     GoalHead: ");
  Serial.print(goalheading);
  Serial.print("     hdavg: ");
  Serial.print(hdavg);
  Serial.print("     Depth: ");
  Serial.print(depth);
  Serial.print("     LoopT: ");
  Serial.println(loopt);
}

//this function prints the coordinates it read off the SD card. only for testing to make sure card is being read correctly, not used during operation. 
void printCoords()
{
  for(n=0;n<=ncoords;n++)
  {
    Serial.print(Carray[0][n],6);
    Serial.print(F(" - "));
    Serial.print(Carray[1][n],6);
    Serial.println(F(" "));
  }
} 

//just for testing purposes, this code checks how long the microcontroller is taking to complete a loop of the main code.
void looptimecheck()  
{
  loopt = millis()-looptlast;
  looptlast = millis();
}

#endif
