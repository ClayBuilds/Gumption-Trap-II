//SDWRITEFROMPC
//Version 2.0, 6/8/24
//This code takes in data over the main USB to copy .txt files coming from a python script running on a PC into the SD card wired to the arudino

//Changes from v1:
/*
-write escs to neutral
*/

//NOTE: See readme in same folder as the associated python script. This file, SDWRITEFROMPC, works with SDWRITETOARDUINO.py

#include <SPI.h>
#include <SD.h>
#include <Servo.h>

Servo port;
Servo starboard;

int pwmlow = 1000;
int pwmhigh = 2000;

const byte pmot = 4;
const byte smot = 3;

const int cs = 10; //cs pin

void setup() 
{
  port.attach(pmot,pwmlow,pwmhigh);
  starboard.attach(smot,pwmlow,pwmhigh);

  port.write(1500);
  starboard.write(1500);


  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for the serial port to connect. Needed for native USB port only
  }

  if (!SD.begin(cs)) {
    Serial.println("Initialization failed!");
    return;
  }
  Serial.println("Initialization done.");
  nuke(SD.open("/"));   //wipe the SD card before starting to write new stuff
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    if (command.startsWith("Start:")) {
      String filename = command.substring(6);
      File file = SD.open(filename.c_str(), FILE_WRITE);
      if (file) {
        //Serial.println("Receiving file: " + filename);
        while (true) {
          if (Serial.available()) {
            String line = Serial.readStringUntil('\n');
            if (line.startsWith("End:")) {
              file.flush();
              file.close();
              //Serial.println("File received: " + filename);
              break;
            } else {
              file.println(line);
              file.flush();
              //file.close();
              //File file = SD.open(filename.c_str(), FILE_WRITE);
            }
          }
          else
          {delay(2);}
        }
      } 
    }
  }
}

void nuke(File dir) {
  while (true) {
    File entry = dir.openNextFile();
    if (!entry) {
      // no more files
      break;
    }
    if (entry.isDirectory()) {
      nuke(entry);
      SD.rmdir(entry.name()); // Remove the directory after deleting its contents
    } else {
      //Serial.print("Deleting file: ");
      //Serial.println(entry.name());
      SD.remove(entry.name());
    }
    entry.close();
  }
}
