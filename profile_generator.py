
from bokeh.layouts import layout
import pandas as pd
import bokeh.plotting as bp
from bokeh.models import ColumnDataSource
from interactive_profiler import define_boundaries, define_elevation_boundaries, stream_map, profile, color_by_variable



#Read stream data
name = "Mandakini_fullProfileMC_forced_0.45_3_1258909000_10_80_281_for_Arc.csv" #Set file name
path = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Test_data/" #Set path to data
df = pd.read_csv(path+name)


source = ColumnDataSource(df) #Define the data source in bokeh

bp.output_file("Interactive_profile.html")#save  html output
#bp.output_notebook()#for use in jupyter notebook


#define a new color scheme
colors = color_by_variable('elevation', source)
source.data['colors']= colors #add a new coloumn to the source dataset to pass into color plot


x_range, y_range = define_boundaries(df)
elev_range = define_elevation_boundaries(source)


plot = stream_map(x_range, y_range, source)
plot2 = profile(elev_range, source, x='flow_distance', y='elevation', title='Stream profile', x_axis_label='Flow distance (m)', y_axis_label = 'Elevation (m)' )
plot3 = profile(elev_range, source, x='chi', y='elevation', title='Chi profile', x_axis_label='Chi (X)', y_axis_label = 'Elevation (m)')


out = layout([[plot],[plot2], [plot3]])

bp.show(out)