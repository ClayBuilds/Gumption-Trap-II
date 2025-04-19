# PlanStripper
# Clay M 
# 4.10.25
# This program takes a .plan file made with QGroundControl and strips it down to a barebones list of gps lat/long pairs
# This is ideal for low memory microcontrollers and puts it exactly in the format my boat, Gumption Trap II, currently uses. 
# The example input file included here is not what I actually used. Made a random new example. 

import os


input_filepath = 'input'
output_filepath = 'output'

filenames = []
for file in os.listdir(input_filepath):
    if os.path.isfile(os.path.join(input_filepath, file)):  #if it's a file
        if(file[-4:] == 'plan'):                            #if it's a .plan file
            filenames.append(file)

def convert(filename):
    output = []
    npairs = 0
    with open(str(os.path.join(input_filepath, filename)),'r') as inputfile:
        lines = inputfile.readlines()
        for i, line in enumerate(lines):
            if('params' in line):
                lat = lines[i + 5]
                lon = lines[i + 6]
                lat = lat.strip()
                lon = lon.strip()
                lat = lat.strip(',')
                lon = lon.strip(',')
                
                if(len(lat)>1):
                    output.append(lat)
                    output.append(lon)
                    npairs += 1

    outputname = filename[0:len(filename) - 5] + '.TXT'

    with open(os.path.join(output_filepath, outputname), 'w') as outputfile:
        outputfile.write(str(npairs) + '\n')
        for o in output:
            outputfile.write(str(o) + '\n')

for filename in filenames:
    convert(filename)
