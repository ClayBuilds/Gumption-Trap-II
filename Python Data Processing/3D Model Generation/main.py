# main.py
# This is the main code used for generating 3d models of depth plots to carve or 3d print

# Version 2
# Changes from last version:
# -make it actually output a "negative" of the scan. So it adds a floor below the measured pond bottom instead of adding a ceiling at the water surface
# -code works as expected but the file actually kinda comes out worse. 

# Note: make sure the input file doesn't add a "ceiling" at water surface level

import os
import numpy as np
import open3d as o3d

# length and width in inches of the actual output file to be printed/carved
output_xy_in = 6
output_z_in = 0.75 #deepest depth of cut from top to the bottom of pocket
bottom_z_thick = 0.25 #thickness to be below the deepest point in the solid model output (inches)

# Read from the file. rawdata is a list of strings, line by line in the input file
rawdata = []
edgedata = []
datainput = 'input/'
for file in os.listdir(datainput):
    if(file == 'pointcloudfeettoscale.txt'):
        with open(datainput + file, 'r') as datain:
            for line in datain:
                rawdata.append(line)
    if('edge' in file):
        with open(datainput + file, 'r') as edgein:
            for line in edgein:
                edgedata.append(line)

# quantify the strings. pointcloudfeet is a list of lists [[x,y,z], ...] representing the 1:1 scale point cloud in feet
pointcloudfeet = []
for line in rawdata:
    linedata = line.split(', ')
    numbers = []
    for number in linedata:
        numbers.append(float(number))
    pointcloudfeet.append(numbers)

edgecloudfeet = []
for line in edgedata:
    linedata = line.split(', ')
    numbers = []
    for number in linedata:
        numbers.append(float(number))
    edgecloudfeet.append(numbers)

# numpy array of the to scale data in feet
pcftarr = np.array(pointcloudfeet) #now columns are x, y, z and there's a row for each datapoint
pcftedge = np.array(edgecloudfeet)

# find max/min/range to use for scaling and scale down the array to the model size
xrange = abs(pcftarr[:,0].max()-pcftarr[:,0].min())
yrange = abs(pcftarr[:,1].max()-pcftarr[:,1].min())
zrange = abs(pcftarr[:,2].max()-pcftarr[:,2].min())
horizontal_max = max(xrange, yrange)
zscalar = output_z_in/zrange
xyscalar = output_xy_in/horizontal_max
pcdownscaled = np.stack((pcftarr[:,0]*xyscalar, pcftarr[:,1]*xyscalar, pcftarr[:,2]*zscalar), axis=1)
edgedownscaled = np.stack((pcftedge[:,0]*xyscalar, pcftedge[:,1]*xyscalar, pcftedge[:,2]*zscalar), axis=1)
# pcdownscaled is now in inches

# Make a pointcloud of the "floor" below every point
floorlist = []
for i in range(0,pcdownscaled[:,2].size):
    floorlist.append([pcdownscaled[i,0], pcdownscaled[i,1], -output_z_in-bottom_z_thick])
floorpcd = np.stack(floorlist)

# Make a pointcloud of the "edge wall"
walllist = []
zspace = np.linspace(0,output_z_in,5)
for i in range(0,edgedownscaled[:,2].size):
    for z in zspace:
        walllist.append([edgedownscaled[i,0], edgedownscaled[i,1], -z])
wallpcd = np.stack(walllist)


# # Main point cloud of main measured depth points
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(pcdownscaled)

# combine data and make a main point cloud
pcd = o3d.geometry.PointCloud()
combined = np.vstack([pcdownscaled, floorpcd, wallpcd])
pcd.points = o3d.utility.Vector3dVector(combined)

# Visualize the raw pointcloud then downsample it to clean up noise a little.
# o3d.visualization.draw_geometries([pcd])
pcddownsampled = pcd.voxel_down_sample(voxel_size = 0.3) #in this case, 0.3 is the length of a voxel in inches. So it will average out all the points within that voxel to one point.
# o3d.visualization.draw_geometries([pcddownsampled])



# Convert to mesh
alpha = 1 # a very small alpha will result in a thin skeleton type shape. Very large will oversimplify and miss some deeper concave areas. Think of it like dropping an alpha radius ball onto the pointcloud and seeing where it touches 3 points
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcddownsampled, alpha)
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh, pcd], mesh_show_back_face=True)

# output the .stl file
# outpath = os.path.join('output', 'output.stl')
# o3d.io.write_triangle_mesh(outpath, mesh)