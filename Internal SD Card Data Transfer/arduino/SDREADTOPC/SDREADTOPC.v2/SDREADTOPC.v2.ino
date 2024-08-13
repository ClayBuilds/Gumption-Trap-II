//SDREADTOPC
//Version 2, 7.3.24
//This code will copy everything from the connected SD card and spit it out to a python script running on a PC

//changes from v1:
/*
-write ESCs to the neutral position
*/

//NOTE: See readme in same folder as the associated python script. This file, SDREADTOPC, works with SDREADFROMARDUINO.py
#include <SPI.h>
#include <SD.h>
#include <Servo.h>

Servo port;
Servo starboard;

int pwmlow = 1000;
int pwmhigh = 2000;

const byte pmot = 4;
const byte smot = 3;

const int cs = 10; // chip select pin for SD card


void setup() 
{
  port.attach(pmot,pwmlow,pwmhigh);
  starboard.attach(smot,pwmlow,pwmhigh);

  port.write(1500);
  starboard.write(1500);

  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for the serial port to connect. 
  }

  if (!SD.begin(cs)) {
    Serial.println("Initialization failed!");
    return;
  }
  Serial.println("Initialization done.");

  // List all files in the root directory
  File root = SD.open("/");
  printDirectory(root, 0);
  root.close();
}

void loop() {
  // Do nothing in the loop
}

void printDirectory(File dir, int numTabs) {
  while (true) {
    File entry = dir.openNextFile();
    if (!entry) {
      // No more files
      break;
    }
    for (uint8_t i = 0; i < numTabs; i++) {
      Serial.print('\t');
    }
    Serial.print(entry.name());
    if (entry.isDirectory()) {
      Serial.println("/");
      printDirectory(entry, numTabs + 1);
    } else {
      // Files have sizes, directories do not
      Serial.print("\t\t");
      Serial.println(entry.size(), DEC);
      if (String(entry.name()).endsWith(".TXT") || String(entry.name()).endsWith(".txt")) 
      {
        // Read and send the file content
        sendFileContent(entry.name());
      }
    }
    entry.close();
  }
}

void sendFileContent(const char *filename) {
  File file = SD.open(filename);
  if (file) {
    Serial.println(String("Start:") + filename);
    while (file.available()) {
      char buffer[64];
      int bytesRead = file.readBytes(buffer, sizeof(buffer));
      Serial.write(buffer, bytesRead);
      delay(10); // Adding a small delay to avoid overflow
    }
    Serial.println(String("End:") + filename);
    file.close();
  } else {
    Serial.println("Error opening " + String(filename));
  }
}
