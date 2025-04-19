# GTII Main Data Processor
# All of this code written for Sensor and Signal Interpretation Final project
# 4/18/2025

# 'Gumption Trap II' (GTII) is an autonomous boat project I have been working on in my spare time for about a year.
# This boat autonomously follows a path along a predetermined set of GPS coordinate waypoints
# It uses a GPS module and a magnetometer as a compass for navigation.
# A PID control loop steers it along its goal heading using a rudder and differential thrust across the two propellers
# The boat is solar powered, operating nominally at about 200W. It also has 20Ah of battery capacity. 
# The purpose of this boat is to create topographical maps of the bottoms of small lakes and ponds.

# Sensors:
# The boat's primary sensor is a sonar echo sounder which measures the depth of the water as the boat drives.
# It has a GPS and magnetometer for navigation
# There is a voltage sensor which monitors the battery voltage
# 2 current sensors monitor the current coming out of the solar panel and the current drawn by the load of the entire system
# the difference between the 2 sensor readings is the current into (+) or out of (-) the battery
# an onboard SD card logs all the data once per second.

# This project will create a python program to autonomously interpret and process the data collected by the boat.
# I have previously done a little bit of data visualization for this in matlab, but I will completely redo and improve it in this python script.
# I'll be working off over several .txt files from data I collected for this project on 4/12/25 from a small lake.
# Example input data files are included. 

import numpy as np
import readrawdata as r
import plotdepth as pd
import coordfuncs as cf
import dataprocessing as dp
import pathplotter as pp


datapath = 'raw data/'
max_reasonable_depth = 50.0 #maximum depth in feet. any values larger than this will be considered erroneous

raw_COORDS, raw_blackbox, raw_depthlog, raw_edge = r.get_raw_lists(datapath)

depthlat = []
depthlon = []
depths = []

#list of erroneous lat, lon, depth points
errpoints = []

#manual deletion indices for points that are obviously wrong after mapping
mandelete = [34, 35, 36, 40, 47, 58, 65, 73,76]

#separate latitude, longitude, and depth out of depthlog
for point in raw_depthlog:
    depthlat.append(point[0])
    depthlon.append(point[1])
    depths.append((point[2]/25.4)/12.0) #convert to ft

#remove an xyz coordinate if the z is errouneous due to extreme depth. 
triple = np.stack([depthlat, depthlon, depths], 1)
erri = []
for i, t in enumerate(triple):
    if t[2] > max_reasonable_depth:
        errpoints.append(t)
        erri.append(i)
errpoints = np.stack(errpoints)
triple = np.delete(triple, erri, 0)

#remove extreme outlier points (GPS outputting 0 or if I turned boat on far from the mission area)
triple = cf.triple_remove_outliers(triple, raw_edge)

#manually delete points that visually are clearly wrong
# for i, trip in enumerate(triple):
#     print(trip)
#     print(i)
triple = np.delete(triple, mandelete, 0)

#x,y, and z list of filtered measurement points 
depthlat = triple[:,0]
depthlon = triple[:,1]
depths = triple [:,2]


#convert to feet
depthx, depthy, origin = cf.latlon2ft(depthlat, depthlon)

#add in edge points
edgex, edgey = cf.formatcoord2xy(raw_edge, origin)
edge0 = [0]*len(edgex)

#combine edge and depth for final map
mapx = depthx + edgex
mapy = depthy + edgey
mapz = -1*np.concatenate([depths, np.array(edge0)])
zscalar = 10 #exagerate z visually
pd.depthplot(mapx, mapy, mapz, zscalar)
# pd.depthplot(depthlat, depthlon, depths)

bbdata = dp.parseBB(raw_blackbox)
dp.plotbb(bbdata)

pp.plotpath(raw_edge, raw_COORDS, raw_blackbox)
