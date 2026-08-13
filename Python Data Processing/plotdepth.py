# This file for plotting the depth plot

import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D

#ensure axis are scaled true to life (it's pretty flat)
def scale_axis(ax, zscalar):
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    plot_radius = 0.5 * max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([(z_middle - plot_radius)/zscalar, (z_middle + plot_radius)/zscalar])

def depthplot(x, y, z, zscalar):
    #create linear grid
    gridsize = 1000
    xi = np.linspace(min(x), max(x), gridsize)
    yi = np.linspace(min(y), max(y), gridsize)
    xi, yi = np.meshgrid(xi, yi)

    #interpolate the surface
    zi = griddata((x,y), z, (xi, yi), method = 'linear')

    #plot interpolated surface
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    surf = ax.plot_surface(xi, yi, zi, cmap = 'viridis', edgecolor = 'none')

    #add in the actual measured points
    ax.scatter(x, y, z, color = 'k', s =1)
    fig.colorbar(surf)
    surf.set_clim(vmin = min(z), vmax = max(z))

    # Show exact values for debugging
    # for xi, yi, zi in zip(x, y, z):
    #     ax.text(xi, yi, zi, f'({xi}, {yi}, {zi})', fontsize=8, color='black')

    # Start with a top down view
    ax.view_init(elev=90, azim = -90)

    scale_axis(ax, zscalar)
    plt.show()