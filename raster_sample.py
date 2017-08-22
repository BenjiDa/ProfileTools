#import and plot raster data using matplotlib
import gdal
import numpy as np
import matplotlib.pyplot as plt


#Import the data
raster_path = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Cache_creek/"
raster = gdal.Open(raster_path + "/Cache_creek_clip.bil")#Get raster data
dem = raster.ReadAsArray()


#This returns a mesh grid of x and y coordinates to plot up a full raster

def full_raster_xy_generator(raster):
    '''This function takes a raster from raster=gdal.Open('raster/path') and outputs a grid of
    x, y data to plot raster'''

    (upper_left_x, x_res, x_rotation, upper_left_y, y_rotation, y_res) = raster.GetGeoTransform()
    dx = x_res
    dy = y_res
    nx, ny = raster.RasterXSize, raster.RasterYSize  # Size of the original raster

    xllcenter = upper_left_x + dx/2  # x coordinate center of lower left pxl
    yllcenter = upper_left_y - dx/2 # y coordinate center of lower left pxl   

    #Create arrays of the x and y coordinates of each pixel (the axes)
    xcoordinates = [x*dx + xllcenter for x in range(nx)]
    ycoordinates = [y*dy + yllcenter for y in range(ny)]

    #Create 2 2d grids describing x and y coordinates
    X,Y = np.meshgrid(xcoordinates, ycoordinates) 


    return X, Y



def raster_subsample_xy_generator(raster, creek_data_df):
    
    '''
    This function generates and x, y grid of a subsample of a full raster that
    only encompasses the stream of interest. This provides a quick way to analyze
    stream data without clipping rasters
    
    raster is the full raster from: raster = gdal.Open('raster/path').
    
    creek_data contains the x and y coordinates from the creek of interest, 
    should be stored as creek_data['x'] and creek_data['y'].

    x_res and y_res are the resoultions of the raster in x and y dimensions.

    nx_creek and ny_creek are the range of x and y that cover the creek.

    xoff and yoff are the number of pixels to start the plot of the raster.

    xsize and ysize are the range of pixels to plot the raster
    '''

    #Use gdal GetGeoTransorm to get important attributes of the raster
    (upper_left_x, x_res, x_rotation, upper_left_y, y_rotation, y_res) = raster.GetGeoTransform()

    #Define the range of the raster to plot that only covers the creek of interest
    nx_creek = max(creek_data_df['x']) - min(creek_data_df['x'])
    ny_creek = max(creek_data_df['y']) - min(creek_data_df['y'])
    xoff = ((min(creek_data_df['x'])-upper_left_x)/x_res).astype(int).item()
    yoff = ((upper_left_y - max(creek_data_df['y']))/x_res).astype(int).item()
    xsize = (nx_creek/x_res).astype(int).item()
    ysize = (ny_creek/x_res).astype(int).item()

    #Select a part of the raster from the full raster to plot
    array_part = raster.ReadAsArray(
        xoff=xoff,
        yoff=yoff,
        xsize=xsize,
        ysize=ysize)
    ##Can use this to test if the raster section is what you want.
    #plt.imshow(array_part)
    #plt.show()

    #Define the center of the upper left pixel of the creek area
    xcenter = min(creek_data_df['x']) + x_res/2  
    ycenter = max(creek_data_df['y']) - y_res/2 
    #Convert pixels into utm coordinates
    xcoordinates = [x*x_res + xcenter for x in range(xsize)]
    ycoordinates = [y*y_res + ycenter for y in range(ysize)]

    #Create a mesh grid of the coordinates for plotting the raster
    X,Y = np.meshgrid(xcoordinates, ycoordinates)
    
    return X, Y, array_part



