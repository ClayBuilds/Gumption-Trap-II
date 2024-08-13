#include "constvars.h"
#include <TinyGPSPlus.h>
#include <Adafruit_LIS2MDL.h>

#ifndef NAVIGATION_H
#define NAVIGATION_H

void navigate()
{
  smartDelay(50); //added this smartDelay to continuously read gps for a short period
  
  /*This if statement only read one byte of gps data per loop
  if (Serial1.available())
    {gps.encode(Serial1.read());}
  */
  if(gps.location.isValid())                  
  {
    currentLat = gps.location.lat();
    currentLong = gps.location.lng();  
  }
  else
  {
    logerror(2);  //loss of GPS data
  }
  
  if(!(gps.location.isUpdated()))
  {
    //logerror(7);  //error if gps isn't updating. This error is unfinished, it triggered constantly when testing so commented out. 
  }
  
  //read raw mag sensor
  sensors_event_t event;  
  mag.getEvent(&event);

  //this formula adds in the calibration offsets, declination, and outputs degrees in +- 180 range.
  currentheading = (((atan2(-(event.magnetic.y-yoff),(event.magnetic.x-xoff)) * 180) / Pi)+declination);

  //convert to azimuth where 0 = due north, 180 = due south, 90 = due east , 270 = due west  
  if (currentheading < 0)
  {currentheading = 360 + currentheading;}
}

#endif