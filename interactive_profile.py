
import numpy as np
import pandas as pd
from osgeo import gdal
from gdalconst import *

import matplotlib.pyplot as plt
#%matplotlib qt #For work in jupyter notebook

#Import bokeh 
from bokeh.plotting import *
from bokeh.models import ColumnDataSource, Label
from bokeh.layouts import layout

#package in this working directory
#from utils.colormap import RGBAColorMapper
import netCDF4
#from bokeh.palettes import RdBu11
#import color palettes for plotting raster
from bokeh.palettes import *



##Read a raster
#path to data
path = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Test_data/"
#name of raster
Test = gdal.Open(path + "/Mandakini.bil")#Get raster data
M_DEM = Test.ReadAsArray()

#Read stream data
#file name
name = "Mandakini_fullProfileMC_forced_0.45_3_1258909000_10_80_281_for_Arc.csv" #Set file name
#for csv files, names are set to predefined output from LSDTopoTools
data = np.genfromtxt((path+name), delimiter=',', skip_header=1, names=['id', 'x', 'y', 'chan_number', 'reciever_chan','node_on_reciever_chan', 'node', 'row','column', 'flow_distance', 'chi', 'elevation', 'drainage_area', 'n_data_points', 'm_mean','m_st_dev', 'm_std_err', 'b_mean', 'b_st_dev', 'b_std_err', 'DW_mean', 'DW_st_dev', 'DW_std_err', 'fitted_elev_mean', 'fitted_elev_stdev', 'fitted_elev_std_err'])
#for tree files
#data = np.genfromtxt((path+name), delimiter=' ', skip_header=1, names=['chan_number', 'reciever_chan','node_on_reciever_chan', 'node', 'row','column', 'flow_distance', 'chi', 'elevation', 'drainage_area', 'n_data_points', 'm_mean','m_st_dev', 'm_std_err', 'b_mean', 'b_st_dev', 'b_std_err', 'DW_mean', 'DW_st_dev', 'DW_std_err', 'fitted_elev_mean', 'fitted_elev_stdev', 'fitted_elev_std_err'])



#My bokeh figure

#m/n ration used in plot, this will need to change based on the name of the .csv or .tree file
mn = name[31:35] #" (m/n = 0.45)"

# output to static HTML file
output_file("linked_brushing.html")

# NEW: create a column data source for the plots to share
stream_source = ColumnDataSource(data=dict(x0=data['flow_distance'], x1=data['chi'], y=data['elevation']))

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"

# create a new plot and add a renderer
left = figure(tools=TOOLS, width=350, height=350, title='Stream Profile')
left.circle('x0', 'y', source=stream_source)
left.xaxis.axis_label = 'Flow Distance (m)'
left.yaxis.axis_label = 'Elevation (m)'

# create another new plot and add a renderer
right = figure(tools=TOOLS, width=350, height=350, title='Chi Profile'+ mn)
right.circle('x1', 'y', source=stream_source)#, legend = "m/n = 0.45")
right.xaxis.axis_label = 'Chi (X)'
right.yaxis.axis_label = 'Elevation (m)'


#Set ranges for DEM image
dw = max(data['x'])- min(data['x'])
dh = max(data['y'])- min(data['y'])
xrmax = max(data['x'])
xrmin = min(data['x'])
yrmax = max(data['y'])
yrmin = min(data['y'])

dem = M_DEM[::-1] #set north-up on DEM, fix a small bug?

#Create Color palette
pal = viridis(256)
pal[0] = '#000000'

topo = figure(plot_height=700, plot_width=700, x_axis_type=None, y_axis_type=None, x_range=[xrmin,xrmax], y_range=[yrmin,yrmax])

topo.image(image=[dem], x=[min(data['x'])], y=[min(data['y'])],dw=[dw], dh=[dh], palette=pal, name='image')
topo.circle(data['x'], data['y'], color='red', size=3)


# put the subplots in a gridplot
p = layout([[left, right], [topo]])



show(p)
