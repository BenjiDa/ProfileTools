#run with command line: bokeh serve --show mle_mn_slider.py



import bokeh.models as bm
import bokeh.plotting as bp

from bokeh.io import curdoc
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure, show

from plotter_functions import *


#Function to import MLE data and create a dataframe with MLE data for all TRIBUTARIES for each M/N Value

creek = "Perkins_creek"
path = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Cache_creek/Previous_LSDTT_version/Channel_extraction/%s/" % creek#Set path to data
fname = creek+'_movern.csv'#name of movern file with all the chi data

#Call to the plotter function
tribs, main_stem, mle_data_merge = group_chi_mle_data(creek, path, fname, mn_values)


mn = '0.5' #to start the plotting somewhere 

colors = color_maker(tribs, mn)


source = bm.ColumnDataSource(
        data=dict(
            x=tribs['m_over_n = %s' % mn],#.values,
            y=tribs.elevation,#,.values,
            c=colors,
            desc=tribs['MLE m/n %s' % mn]# % mn]#.values
        )
    )

source_ms = bm.ColumnDataSource(
            data=dict(
                x=main_stem['m_over_n = %s' % mn],# % mn],#.values,
                y=main_stem.elevation))#.values))

hover = bm.HoverTool(
        tooltips=[
            ("MLE", "@desc"),
        ]
    )

pan = bm.PanTool()
zoom = bm.WheelZoomTool()

p = bp.figure(plot_height=250, plot_width=500, title=creek, x_axis_label='Chi (X)', y_axis_label='Elevation (m)', 
              tools=[pan, zoom, hover])
p.circle(x='x', y='y', fill_color='darkgray', line_color=None, source=source_ms)
p.circle(x='x', y='y', fill_color='c', size=8, line_color=None, source=source)



# # Set up widgets
mn_values_slider = Slider(title="m/n values", value=0.5, start=0.1, end=0.8, step=0.1)


# Set up callbacks
def update_data(attrname, old, new):

    # Get the current slider values
    mn = mn_values_slider.value

    # Generate the new curve
    xtrib = tribs['m_over_n = %s' % mn]#.values
    ytrib = tribs.elevation#.values
    desc = tribs['MLE m/n %s' % mn]
    xms = main_stem['m_over_n = %s' % mn]#.values
    yms = main_stem.elevation#.values

    colors = color_maker(tribs, mn)
   
    source_ms.data = dict(x=xms, y=yms)   
    source.data = dict(x=xtrib, y=ytrib, c= colors, desc=desc)

    

for mn in [mn_values_slider]:
    mn.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(mn_values_slider)

curdoc().add_root(column(inputs, p, width=800))
curdoc().title = "m/n values"








