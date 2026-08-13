import os
import numpy as np

def get_raw_lists(datapath):
    raw_COORDS = []
    raw_blackbox = []
    raw_depthlog = []
    raw_edge = []

    for file in os.listdir(datapath):

        #parse the coordinate waypoint lines into a list
        if 'COORDS' in file:
            with open(datapath + file, 'r') as coordsfile:
                lines = coordsfile.readlines()
                for line in lines:
                    #the first line is just the integer number of coordinate pairs so I'll ignore it. I may not include that in the future, so this if statement keeps it backwards compatible
                    if not float(line).is_integer():
                        raw_COORDS.append(float(line.strip()))

        if 'edge only' in file:
            with open(datapath + file, 'r') as edgefile:
                lines = edgefile.readlines()
                for line in lines:
                    #the first line is just the integer number of coordinate pairs so I'll ignore it. I may not include that in the future, so this if statement keeps it backwards compatible
                    if not float(line).is_integer():
                        raw_edge.append(float(line.strip()))
           
        #parse the blackbox data into a list
        if 'blackbox' in file:
            with open(datapath + file, 'r') as blackboxfile:
                lines = blackboxfile.readlines()
                for line in lines:
                    line = line.split(', ')
                    linevalid = True
                    for i, val in enumerate(line):
                        line[i] = val.strip()
                        # Remove erroneous entries that contain strings. This sometimes occurrs due to a bug in my program that reads the data off of the boat after a mission. 
                        try:
                            line[i] = float(val)
                        except:
                            linevalid = False
                    if(linevalid):        
                        raw_blackbox.append(line)

        #parse the depthlog data into a list
        if 'depthlog' in file:
            with open(datapath + file, 'r') as depthlogfile:
                lines = depthlogfile.readlines()
                for line in lines:
                    line = line.split(', ')
                    linevalid = True
                    for i, val in enumerate(line):
                        line[i] = val.strip()
                        # Remove erroneous entries that contain strings. This sometimes occurrs due to a bug in my program that reads the data off of the boat after a mission. 
                        try:
                            line[i] = float(val)
                        except:
                            linevalid = False
                    if(linevalid):        
                        raw_depthlog.append(line)

    # These 2 files might have incomplete or doubled up lines if the data recording suddenly starts/stops due to power cycling at the wrong time. 
    # Remove lists that aren't at the median length.                     
    bblmedian = 0
    bbllengths = []
    depmedian = 0
    deplengths = []

    for i in raw_blackbox:
        bbllengths.append(len(i))
    bblmedian = np.median(bbllengths)

    for i in reversed(raw_blackbox):
        if len(i) != bblmedian:
            raw_blackbox.remove(i)

    for i in raw_depthlog:
        deplengths.append(len(i))
    depmedian = np.median(deplengths)

    for i in reversed(raw_depthlog):
        if len(i) != depmedian:
            raw_depthlog.remove(i)
            

    return raw_COORDS, raw_blackbox, raw_depthlog, raw_edge