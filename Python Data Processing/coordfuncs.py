# functions for manipulating xyz coordinates (depth, gps, etc.)
import numpy as np

# convert latitude/longitude to cartesian feet in linear distance
def latlon2ft(lat, lon, origin = [0,0]):
    #pick the origin as the min longitude min latitude if it isn't defined
    lat0 = 0
    lon0 = 0
    if sum(origin) == 0:
        lat0 = min(lat)
        lon0 = min(lon)
    else:
        lat0 = origin[0]
        lon0 = origin[1]
    x = []
    y = []
    R_earth = 20925524.9 #radius of the earth in ft
    lat0rad = np.radians(lat0)
    lon0rad = np.radians(lon0)
    #convert to ft
    for i in range(len(lat)):
        lonrad = np.radians(lon[i])
        latrad = np.radians(lat[i])
        x.append(R_earth*(lonrad-lon0rad)*np.cos(lat0rad))
        y.append(R_earth*(latrad-lat0rad))

    origin = [lat0, lon0]
    return x, y, origin

#take data as it is written to the .txt files and parse it into neat lists output in units of feet
def formatcoord2xy(coords, origin):
    lat = []
    lon = []
    for i, coord in enumerate(coords):
        if i%2 == 0:
            lat.append(coord)
        else:
            lon.append(coord)
    x, y, o = latlon2ft(lat, lon, origin)
    
    return x, y,

#take data as it is written on the .txt files and parse it into neat lists output in units of degrees latitude/longitude
def formatcoord2latlon(coords):
    lat = []
    lon = []
    for i, coord in enumerate(coords):
        if i%2 == 0:
            lat.append(coord)
        else:
            lon.append(coord)
    return lat, lon

#form upper and lower boundaries for latitude/longitude in a square around the edge of the lake
def get_edge_bounds(edgepoints):
    lat = []
    lon = []
    for i, point in enumerate(edgepoints):
        if i%2 == 0:
            lat.append(point)
        else:
            lon.append(point)
    latbounds = [min(lat), max(lat)]
    lonbounds = [min(lon),max(lon)]
    return latbounds, lonbounds

#eliminate coordinates that are outside the bounding box for the edge of the lake. These get added to the logs if I power the boat on far away, or GPS reads 0,0 initially. 
def triple_remove_outliers(triples, edgebounds):
    latbounds, lonbounds = get_edge_bounds(edgebounds)
    latlowerbound = latbounds[0]
    latupperbound = latbounds[1]
    lonlowerbound = lonbounds[0]
    lonupperbound = lonbounds[1]

    outlierindexes = []
    for i, triple in enumerate(triples):
        if(triple[0]<latlowerbound) or (triple[0]>latupperbound):
            outlierindexes.append(i)
        elif(triple[1]<lonlowerbound) or (triple[1]>lonupperbound):
            outlierindexes.append(i)

    return np.delete(triples, outlierindexes, 0)
    