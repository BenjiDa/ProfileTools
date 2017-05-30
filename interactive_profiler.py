import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm
import bokeh.plotting as bp
from bokeh.models import ColumnDataSource, DataRange1d
from bokeh.models import HoverTool
#from bokeh.layouts import layout



# define boundaries of the plot area, default is adding on 1 km to easting and northing
def define_boundaries(df, r=1000):
    xmin = df['x'].min()
    xmax = df['x'].max()
    ymin =df['y'].min()
    ymax = df['y'].max()
    x_range = (xmin-r, xmax+r)
    y_range = (ymin-r, ymax+r)	
    return x_range, y_range


#define elevation boundaries for profile plots to use for interactive zooming
def define_elevation_boundaries(source_name, r=1000):
    zmin=min(source_name.data['elevation'])
    zmax=max(source_name.data['elevation'])
    elevation_range = DataRange1d(bounds=(zmin-r, zmax+r))
    return elevation_range


#using matplot lib colors in bokeh, change colors by variable in source dataset
def color_by_variable(cbv, source):
    colors = ["#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in 255*mpl.cm.jet(mpl.colors.Normalize()(source.data[cbv]))]
    return colors



#Creating plots
#define tools to use
TOOLS = "pan,wheel_zoom,reset,save,lasso_select"

def stream_map(x_range, y_range, source, x='x', y='y', plot_width=600, plot_height=300, title='Title', x_axis_label='Label', y_axis_label='Label'):
    
    plot = bp.figure(plot_width=plot_width, plot_height=plot_height,x_range=x_range, y_range=y_range, title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
    cr = plot.circle(x='x', y='y', size=20,
                     fill_color="grey", hover_fill_color="firebrick",
                     fill_alpha=0.03, hover_alpha=0.3,
                     line_color=None, hover_line_color="white", source=source)
    plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
    plot.circle(x='x', y='y', size=2, color='colors', source=source)
    return plot



def profile(elev_range, source, x='flow_distance', y='elevation', plot_width=500, plot_height=250, toolbar_location='above', title='Title', x_axis_label='Label', y_axis_label='Label'):
    
 
    plot = bp.figure(plot_width=500, plot_height=250, toolbar_location='above', 
                     title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label, y_range=elev_range)
    
    cr = plot.circle(x=x, y=y, size=20,
                     fill_color='grey', hover_fill_color="firebrick",
                     fill_alpha=0.03, hover_alpha=0.3,
                     line_color=None, hover_line_color="white", source=source)
    plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
    plot.circle(x=x, y=y, size=2, color='colors', source=source) 
    return plot
    




