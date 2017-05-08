#import and plot raster data using matplotlib


#Import the data

#Read a raster
Test_data = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Test_data/"
Test = gdal.Open(Test_data + "/Mandakini.bil")#Get raster data
M_DEM = Test.ReadAsArray()

#Read stream data
name = "Mandakini_fullProfileMC_forced_0.45_3_1258909000_10_80_281_for_Arc.csv" #Set file name
path = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Test_data/" #Set path to data
#for csv files
data = np.genfromtxt((path+name), delimiter=',', skip_header=1, names=['id', 'x', 'y', 'chan_number', 'reciever_chan','node_on_reciever_chan', 'node', 'row','column', 'flow_distance', 'chi', 'elevation', 'drainage_area', 'n_data_points', 'm_mean','m_st_dev', 'm_std_err', 'b_mean', 'b_st_dev', 'b_std_err', 'DW_mean', 'DW_st_dev', 'DW_std_err', 'fitted_elev_mean', 'fitted_elev_stdev', 'fitted_elev_std_err'])
#for tree files
#data = np.genfromtxt((path+name), delimiter=' ', skip_header=1, names=['chan_number', 'reciever_chan','node_on_reciever_chan', 'node', 'row','column', 'flow_distance', 'chi', 'elevation', 'drainage_area', 'n_data_points', 'm_mean','m_st_dev', 'm_std_err', 'b_mean', 'b_st_dev', 'b_std_err', 'DW_mean', 'DW_st_dev', 'DW_std_err', 'fitted_elev_mean', 'fitted_elev_stdev', 'fitted_elev_std_err'])





def plot_coord(Test):

    (upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size) = Test.GetGeoTransform()
    dx = x_size
    dy = y_size
    nx, ny = Test.RasterXSize, Test.RasterYSize  # Size of the original raster

    xllcenter = upper_left_x + dx/2  # x coordinate center of lower left pxl
    yllcenter = upper_left_y - dx/2 # y coordinate center of lower left pxl   - (ny-1)*dx 

    #Create arrays of the x and y coordinates of each pixel (the axes)
    xcoordinates = [x*dx + xllcenter for x in range(nx)]
    ycoordinates = [y*dy + yllcenter for y in range(ny)]

    #Create 2 2d grids describing x and y coordinates
    X,Y = np.meshgrid(xcoordinates, ycoordinates) 


    fig = plt.contourf(X, Y, M_DEM, levels=np.linspace(np.amin(M_DEM[M_DEM > 0]),np.amax(M_DEM), 50))

    return X, Y, fig


plot_coord(Test)