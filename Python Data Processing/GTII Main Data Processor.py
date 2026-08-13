# GTII Main Data Processor
# Version 3
# 11/29/2025

# Changes from previous version:
# -add function to output .txt pointcloud with final trimmed depth map

# REMEBER don't upload obscure_coords publicly

import numpy as np
import readrawdata as r
import plotdepth as pd
import coordfuncs as cf
import dataprocessing as dp
import pathplotter as pp
import pointcloudout as pc


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

# pd.depthplot(mapx, mapy, mapz, zscalar)
# # pd.depthplot(depthlat, depthlon, depths)

# bbdata = dp.parseBB(raw_blackbox)
# dp.plotbb(bbdata)

# pp.plotpath(raw_edge, raw_COORDS, raw_blackbox)

pc.pcout(mapx, mapy, mapz)
pc.pcedgeout(edgex, edgey)