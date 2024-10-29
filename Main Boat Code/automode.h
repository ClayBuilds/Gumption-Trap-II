//this file for autonomous mission control
#include "constvars.h"
#include "miscfuncs.h"
#include "cardlogger.h"

#ifndef AUTO_MODE_h
#define AUTO_MODE_h

void automode()
{
  
//plot a course from current location to goal location (degrees heading)
  goalLat = Carray[0][waypoint];
  goalLong = Carray[1][waypoint];
  goalheading = TinyGPSPlus::courseTo(currentLat,currentLong,goalLat,goalLong);  
  
 
  //current heading is in azimuth where 0 = due north, 180 = due south, 90 = due east , 270 = due west
  //goal heading is the same
  
  hdiff = currentheading-goalheading;     //hdiff is the "error" for the PID. It's how far off the goal is from the actual heading. This error should be kept at zero, the setpoint.
  
  //the following two statements handle any weirdness if goal and current are on opposite sides of 0, i.e. if it's 358 degrees minus 2 degrees, that shouldn't be a 356 degree turn.
  if(hdiff>180)   //so that it won't try ant turn around the "long" way left
  {hdiff-=360;}
  
  if(hdiff<(-180))  //so that it won't try and turn around the "long" way right
  {hdiff+=360;}
  
  //hdiff rolling average to smooth out sudden random jumps
  for(int i = 0; i<4; i++)
  {hdarr[i] = hdarr[i+1];}
  
  hdarr[4] = hdiff;
  
  hdsum = 0;
  for(int i = 0; i<5; i++)
  {hdsum = hdsum + hdarr[i];}
  
  hdavg = hdsum/5;
  
  //set pid input based on heading error. note: hdiff>0 left turn, hdiff<0 right turn
  PIDInput = hdavg;
  //at this point the PIDInput, is in the range of +/- 180 degrees
  
  //default motors to full throttle forward
  goalport = pwmhigh;
  goalstarb = pwmhigh;
  
  //always use the rudder. Note that it maxes out early when PIDOutput is +-50. More extreme PID outputs will bring differential thrust into play also. 
  rudval = map(PIDOutput, -50, 50, servlow, servhigh);
  //goalrud = map(PIDOutput, -50, 50, servlow, servhigh);
  
  if(PIDOutput > 50) //differential thrust for hard right turn when PID output is extreme
  {
    //leave port value maxed, subtract libearly from starboard potentially up to full reverse
    goalstarb = goalstarb - map(PIDOutput, 50, 100, 0, (pwmhigh-pwmlow));
  }
  if(PIDOutput < -50) //differential thrust for hard left turn when PID output is extreme
  {
    //leave starboard value maxed, subtract libearly from port potentially up to full reverse
    goalport = goalport - map(PIDOutput, -50, -100, 0, (pwmhigh-pwmlow));
  }
  
  if(abs(hdiff)<10)       //check if it's close to target
  {lastgoodhead = millis();}
  
  if(millis()-lastgoodhead>60000) //log an error if it goes more than 60 seconds without reaching its target heading
  {logerror(3);}
  
  //safeguards to prevent out of bounds pwm output
  if(goalport>pwmhigh)
  {goalport = pwmhigh;}
  if(goalstarb>pwmhigh)
  {goalstarb = pwmhigh;}

  if(goalport<pwmlow)
  {goalport = pwmlow;}
  if(goalstarb<pwmlow)
  {goalstarb = pwmlow;}
  
  if(rudval>servhigh)
  {rudval = servhigh;}
  if(rudval<servlow)
  {rudval = servlow;}
/*
  if(goalrud>servhigh)
  {goalrud = servhigh;}
  if(goalrud<servlow)
  {goalrud = servlow;}
  
  rudder smooth ramping up/down commented out for now, just discretely going immediately to goal value.
*/
  
  //set the motors to their determined throttles 
  adjustpwm(goalport, 0);              
  adjustpwm(goalstarb, 1);
  rudder.writeMicroseconds(rudval);
  //adjustpwm(goalrud, 2);

  d = gps.distanceBetween(currentLat, currentLong, goalLat, goalLong);      //check if you made it to a waypoint
  if ((d<12)&&(waypoint<ncoords))
  {waypoint++;}
}

#endif