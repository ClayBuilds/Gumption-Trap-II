# This program plots the gps coordinates, real and planned, that the robot followed

import coordfuncs as cf
import matplotlib.pyplot as plt
import numpy as np

def plotpath(edge, plan, run):
    #pull GPS lat lon coords out of blackbox
    pathlat = []
    pathlon = []
    for val in run:
        pathlat.append(val[2])
        pathlon.append(val[3])        
    
    #remove the far off outliers
    doubles = np.stack([pathlat, pathlon], 1)
    doubles = cf.triple_remove_outliers(doubles, edge)

    #parse the coordinates of the edge map and the waypoint plan 
    edgelat, edgelon = cf.formatcoord2latlon(edge)
    planlat, planlon = cf.formatcoord2latlon(plan)

    #append first value to the end so its continuous loop
    edgelat.append(edgelat[0])
    edgelon.append(edgelon[0])
    
    pathlat = doubles[:,0]
    pathlon = doubles[:,1]

    plt.figure(figsize=(12,12))
    plt.plot(edgelat, edgelon, color = 'red', label = 'Shore')
    plt.plot(planlat, planlon, color = 'black', label = 'Planned Path')
    plt.plot(pathlat, pathlon, color = 'green', label = 'Actual Path')

    #in this hemisphere, longitude increases east to west
    plt.gca().invert_xaxis()

    plt.legend()
    plt.title('Planned vs Actual Path')
    plt.xlabel('Latitude (Degrees)')
    plt.ylabel('Longitude (Degrees)')
    plt.tight_layout()
    plt.show()

