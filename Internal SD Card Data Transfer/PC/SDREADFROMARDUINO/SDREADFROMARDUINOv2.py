#SDREADFROMARDUINO Version 2
#6/8/24
#This code copies all the data coming from an SD card connected to an arduino which outputs it over its main USB cable.
#tested with arduino code "SDREADTOPC.v1"
#works pretty well, but has some extra characters in the files it copies. The files copy succesfully but add some stuff that seems to just be filenames of the next ones for some reason.

import serial
import time
import os

serial_port = 'COM3'  # Arduino serial port (3 on laptop 4 on desktop)
baud_rate = 9600

output_directory = 'sd_card_files'
os.makedirs(output_directory, exist_ok=True)

def read_from_serial(ser):
    file = None
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Line read: {line}")  # Debug print
            if line.startswith('Start:'):
                filename = line.split(':')[1]
                file_path = os.path.join(output_directory, filename)
                file = open(file_path, 'w')  # Open in text mode
                print(f"Receiving file: {filename}")
            elif line.startswith('End:'):
                if file:
                    file.close()
                    print(f"File received: {filename}")
                    file = None
            else:
                # Write the line to the file immediately
                if file:
                    print(f"Writing to file: {line}")  # Debug print
                    file.write(line + '\n')
                    file.flush()  # Ensure data is written to disk immediately

if __name__ == '__main__':
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        print("Serial connection established")  # Debug print
        time.sleep(2)  # Wait for the serial connection to initialize
        read_from_serial(ser)