# pointcloudout.py

# This code is for outputting a clean x,y,z pointcloud of parsed/trimmed data that can later be used to generate an .stl for printing or carving
def pcout(cloudx, cloudy, cloudz):
    output_path = "outputs/pointcloudfeettoscale.txt"
    with open(output_path, "w") as file:
        for i in range(0,len(cloudx)):
            if(cloudz[i] == 0):
                file.write(str(cloudx[i]) + ', ' + str(cloudy[i]) + ', ' + '0.0' + '\n') #solves the problem of it printing negative zero as -0.0
            else:
                file.write(str(cloudx[i]) + ', ' + str(cloudy[i]) + ', ' + str(cloudz[i]) + '\n') 
                # file.write(str(cloudx[i]) + ', ' + str(cloudy[i]) + ', ' + '0.0' + '\n') #uncomment this if you want a "ceiling" added to the point cloud at water surface level

def pcedgeout(edgex, edgey):
    output_path = "outputs/edgeonly.txt"
    with open(output_path, "w") as file:
        for i in range(0,len(edgex)):
            file.write(str(edgex[i]) + ', ' + str(edgey[i]) + ', 0.0\n')