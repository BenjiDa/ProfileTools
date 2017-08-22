import numpy as np
import pandas as pd
import utm
import matplotlib as mpl
import matplotlib.cm as cm
import bokeh.plotting as bp
from bokeh.models import ColumnDataSource, DataRange1d
from bokeh.models import HoverTool
from bokeh.palettes import Viridis256 as v256
#from bokeh.layouts import layout

# define boundaries of the plot area, default is adding on 1 km to easting and northing
def define_boundaries(source, r=1000):
    xmin = source.data['x'].min()
    xmax = source.data['x'].max()
    ymin = source.data['y'].min()
    ymax = source.data['y'].max()
    x_range = (xmin-r, xmax+r)
    y_range = (ymin-r, ymax+r)  
    return x_range, y_range


#define elevation boundaries for profile plots to use for interactive zooming
def define_elevation_boundaries(source, r=1000):
    zmin=min(source.data['elevation'])
    zmax=max(source.data['elevation'])
    elevation_range = DataRange1d(bounds=(zmin-r, zmax+r))
    return elevation_range


#using matplot lib colors in bokeh, change colors by variable in source dataset
def color_by_variable(cbv, source):
    colors = ["#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in 255*mpl.cm.coolwarm(mpl.colors.Normalize()(source.data[cbv]))]
    source.data['colors'] = colors
    return colors

#convert the lat long to utm from creek data if not x,y columns exist, requires utm package
def convert_lat_long(creek_data_df):
    x = []
    tup = []
    y = []

    for i in range(0,len(creek_data_df)):
        xi = utm.from_latlon(creek_data_df['latitude'][i], creek_data_df['longitude'][i])
        tup.append(xi)
        x_fin = tup[i][0]
        y_fin = tup[i][1]
        x.append(x_fin)
        y.append(y_fin)

    xd = pd.DataFrame(x, columns=['x'])
    yd = pd.DataFrame(y, columns=['y'])
    xdyd = pd.concat([xd, yd],axis=1)
    creek_data_df_new = pd.concat([creek_data_df,xdyd],axis=1)
    
    return creek_data_df_new


#Creating plot functions
#define tools to use
#TOOLS = "pan,wheel_zoom,reset,save,lasso_select"

def stream_map(x_range, y_range, source, x='x', y='y', plot_width=600, plot_height=300, title='Title', x_axis_label='Label', y_axis_label='Label'):
    
    plot = bp.figure(plot_width=plot_width, plot_height=plot_height,x_range=x_range, y_range=y_range, title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
    cr = plot.circle(x='x', y='y', size=20,
                     fill_color="grey", hover_fill_color="firebrick",
                     fill_alpha=0.03, hover_alpha=0.3,
                     line_color=None, hover_line_color="white", source=source)
    plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
    plot.circle(x='x', y='y', size=2, color='colors', source=source)
    
    return plot


def stream_map_raster(array, source, plot_width=600, plot_height=300, title='Title', x_axis_label='Label', y_axis_label='Label'):
    
    plot = bp.figure(x_range=(min(source.data['x']), max(source.data['x'])), y_range=(min(source.data['y']), max(source.data['y'])))
    d = array[::-1, :]#flip array for rasters
    plot.image(image=[d], x=min(source.data['x']), y=min(source.data['y']), dw=max(source.data['x']) - min(source.data['x']), dh=max(source.data['y']) - min(source.data['y']), palette=v256)
    cr = plot.circle(x='x', y='y', size=10,
                     fill_color='grey', hover_fill_color="firebrick",
                     fill_alpha=0.03, hover_alpha=0.3,
                     line_color=None, hover_line_color="white", source=source)
    plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
    plot.circle(x='x', y='y', size=2, source=source)
    
    return plot



def profile(elev_range, source, x='distance', y='elevation', plot_width=500, plot_height=250, toolbar_location='above', title='Title', x_axis_label='Label', y_axis_label='Label'):
    
 
    plot = bp.figure(plot_width=500, plot_height=250, toolbar_location='above', 
                     title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label, y_range=elev_range)
    
    cr = plot.circle(x=x, y=y, size=10,
                     fill_color='grey', hover_fill_color="firebrick",
                     fill_alpha=0.03, hover_alpha=0.3,
                     line_color=None, hover_line_color="white", source=source)
    plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
    plot.circle(x=x, y=y, size=2, fill_color='colors', line_color=None, source=source) 
    
    return plot
