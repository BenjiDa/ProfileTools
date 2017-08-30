#run with command line: bokeh serve --show mn_ratio_slider.py

import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure, show


#Function to import MLE data and create a dataframe with MLE data for all TRIBUTARIES for each M/N Value

creek = "Perkins_creek"
path = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Cache_creek/Previous_LSDTT_version/Channel_extraction/%s/" % creek#Set path to data
fname = creek+'_movern.csv'#name of movern file with all the chi data

#Create a function to pull in MLE data
mn_values = [x / 10.0 for x in range(1, 9, 1)]#create a list of floats.


def group_chi_mle_data(creek, path, fname, mn_values):
    #Import Chi Data
    movern_df = pd.read_csv((path+name), delimiter=',', header=0, names=['source_key','basin_key','elevation','m_over_n = 0.1','m_over_n = 0.2','m_over_n = 0.3','m_over_n = 0.4','m_over_n = 0.5','m_over_n = 0.6','m_over_n = 0.7','m_over_n = 0.8'])
    movern_df = movern_df.rename(columns={'source_key': 'Tributary'})
    movern_df_tribs = movern_df[movern_df['Tributary']!=0]
    movern_df_ms = movern_df[movern_df['Tributary']==0]

    #import MLE Data and merge with Chi
    mle_data_i = []
    mle_data_merge = pd.DataFrame()
    for mn in mn_values:

        movern_df = pd.read_csv((path+name), delimiter=',', header=0, names=['source_key','basin_key','elevation','m_over_n = 0.1','m_over_n = 0.2','m_over_n = 0.3','m_over_n = 0.4','m_over_n = 0.5','m_over_n = 0.6','m_over_n = 0.7','m_over_n = 0.8'])
        movern_df = movern_df.rename(columns={'source_key': 'Tributary'})
        movern_df_tribs = movern_df[movern_df['Tributary']!=0]


        full_name = '%s%s_movernstats_%s_fullstats.csv' % (path, creek, mn)

        name_mle = 'MLE m/n %s' % mn
        name_rmse = 'RMSE m/n %s' % mn

        mle_data = pd.read_csv(full_name, delimiter=',', header= 0,names=['basin_key', 'reference_source_key', 'test_source_key','MLE','RMSE'])

        mle_data = pd.DataFrame(mle_data)
        mle_data_i.append(mle_data)

        mle_data_merge['test_source_key'] = mle_data['test_source_key']
        mle_data_merge[name_mle] = mle_data['MLE']
        mle_data_merge[name_rmse] = mle_data['RMSE']

        movern_df_tribs_merge = movern_df_tribs.merge(mle_data_merge, left_on = "Tributary", right_on = "test_source_key")

    return movern_df_tribs_merge, movern_df_ms


tribs, main_stem = group_chi_mle_data(creek, path, fname, mn_values)


#assign bokeh data sources
souce_tribs = ColumnDataSource(tribs)
source = ColumnDataSource(main_stem)


# Set up plot
plot = figure(plot_height=250, plot_width=500, title=creek, x_axis_label='Chi (X)', y_axis_label='Elevation (m)',
              tools="pan,reset,save,wheel_zoom")
plot.circle('m_over_n = 0.1', 'elevation', source=source_ms)

#show(plot)
# # Set up widgets
mn_values_slider = Slider(title="m/n values", value=0.0, start=0.1, end=0.8, step=0.1)


# Set up callbacks
def update_data(attrname, old, new):

    # Get the current slider values
    mn = mn_values_slider.value


    # Generate the new curve
    x = source_ms.data['m_over_n = %s' % mn]['chi']
    y = source_ms.data['elevation']

    source_ms.data = dict(x=x, y=y)

for mn in [mn_values_slider]:
    mn.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(mn_values_slider)

curdoc().add_root(column(inputs, plot, width=800))
curdoc().title = "m/n values"









