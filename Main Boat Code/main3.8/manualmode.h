//this file for manual drive control code with an RC transmitter
#include "constvars.h"
#include "pindefinitions.h"
#include "miscfuncs.h"

#ifndef MANUAL_MODE_h
#define MANUAL_MODE_h

void manualmode()
{
  //read pwm inputs from rc receiver
  throtval = readChannel(throt, -100,100,0);
  steerval = readChannel(steer, -100,100,0);
  
  //safeguard to make throttle zero if stick holds it barely off zero
  if(abs(throtval)<5)
  {
    throtval = 0;
    goalport = pwmmid;
    goalstarb = pwmmid;
  }
  else  //linearly map motor values based on throttle value
  {
    goalport = (map(throtval, -100,100,pwmlow,pwmhigh));
    goalstarb = (map(throtval, -100,100,pwmlow,pwmhigh));
  }
  
  //use differential thrust for high steering input values
  if(steerval > 50) //hard right turn
  {
    goalstarb = goalstarb - map(steerval, 50, 100, 0, (pwmmid-pwmlow));
    goalport = goalport + map(steerval, 50, 100, 0, (pwmhigh-pwmmid));
  }
  
  if(steerval < (-50))  //hard left turn
  {
    goalport = goalport - map(steerval, -50, -100, 0, (pwmmid-pwmlow));
    goalstarb = goalstarb + map(steerval, -50, -100, 0, (pwmhigh-pwmmid));
  }
  
  //set rudder pwm based on steering input value. rudder hits its max travel with only half stick on the steering input. goes into differential thrust after that.
  rudval = map(steerval, -50, 50, servlow, servhigh);

  
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

  //change wether adjust or write is commented out to use ramp up/ramp down or to directly control pwm value. 
  
  //port.writeMicroseconds(portval);
  //starboard.writeMicroseconds(starbval);
  rudder.writeMicroseconds(rudval);
  
  adjustpwm(goalport, 0);              
  adjustpwm(goalstarb, 1);
  //adjustpwm(goalrud, 2);
}

#endif