#SDWRITETOARDUINO
#Version 1, 6/8/24
#this program takes some existing .txt files from the PC and sends them to an arduino over serial. 
#note: if files of the same name already exist on the SD card, this program will append to the end of them rather than overwrite. arduino program will be configured to delete old contents before writing what it receives from this script
#tested and everything works as intended

import serial
import os
import time

# Replace with your actual serial port and baud rate
serial_port = 'COM3'  # Update this to your Arduino's serial port. port 3 on my laptop, 4 on my desktop
baud_rate = 9600
folder_path = './filestosend'  # Update this to the path of your folder containing .txt files

def send_files_to_arduino(ser, folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt') or filename.endswith('.TXT'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                print(f"Sending file: {filename}")
                ser.write(f"Start:{filename}\n".encode('utf-8'))
                for line in file:
                    ser.write(line.encode('utf-8'))
                    print(line.encode('utf-8'))
                    #time.sleep(.001)
                ser.write(f"End:{filename}\n".encode('utf-8'))
                time.sleep(1)  # Small delay to ensure the Arduino can process the file

if __name__ == '__main__':
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        print("Serial connection established")
        time.sleep(2)  # Wait for the serial connection to initialize
        send_files_to_arduino(ser, folder_path)
        print("All files sent")
