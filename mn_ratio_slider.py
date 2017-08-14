
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

# Set up data
path = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Cache_creek/Previous_LSDTT_version/Channel_extraction/Perkins_creek/" #Set path to data

mnvalues = [0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625]

all_data = {}
for mn in mnvalues:
    name = "Cache_creek_clip_fullProfileMC_forced_"+str(mn)+"_20_-4924088_20_90_3010.tree" #Set file name
    data = np.genfromtxt((path+name), delimiter=' ', skip_header=1, names=['chan_number', 'reciever_chan','node_on_reciever_chan', 'node', 'row','column', 'flow_distance', 'chi', 'elevation', 'drainage_area', 'n_data_points', 'm_mean','m_st_dev', 'm_std_err', 'b_mean', 'b_st_dev', 'b_std_err', 'DW_mean', 'DW_st_dev', 'DW_std_err', 'fitted_elev_mean', 'fitted_elev_stdev', 'fitted_elev_std_err'])
    all_data[mn] = data


source = ColumnDataSource(data=dict(x=all_data[0.5]['chi'], y=all_data[0.5]['elevation']))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="m/n values",x_axis_label='Chi (X)', y_axis_label='Elevation (m)',
              tools="pan,reset,save,wheel_zoom")

plot.circle('x', 'y', source=source)


# Set up widgets
mn_values = Slider(title="m/n values", value=0.0, start=0.15, end=0.625, step=0.025)


# Set up callbacks
def update_data(attrname, old, new):

    # Get the current slider values
    mn = mn_values.value


    # Generate the new curve
    x = all_data[mn]['chi']
    y = all_data[mn]['elevation']

    source.data = dict(x=x, y=y)

for mn in [mn_values]:
    mn.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(mn_values)

curdoc().add_root(column(inputs, plot, width=800))
curdoc().title = "m/n values"
