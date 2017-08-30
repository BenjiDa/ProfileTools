#run with command line: bokeh serve --show mn_ratio_slider.py

import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure


#Function to import MLE data and create a dataframe with MLE data for all TRIBUTARIES for each M/N Value

creek = "Perkins_creek"
path = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Cache_creek/Previous_LSDTT_version/Channel_extraction/%s/" % creek#Set path to data
name = creek+'_movern.csv'#name of movern file with all the chi data

#Create a function to pull in MLE data
mn_values = [x / 10.0 for x in range(1, 9, 1)]#create a list of floats.


def create_MLE_data(mn_values):
    TributariesMLE = []
    mle_data_i = []
    for mn in mn_values: 
        num = mn
        full_name = '%s%s_movernstats_%s_fullstats.csv' % (path, creek, num)

        name_mle = 'MLE m/n %s' % num
        name_rmse = 'RMSE m/n %s' % num

        mle_data = pd.read_csv(full_name, delimiter=',', header= 0,names=['basin_key', 'reference_source_key', 'test_source_key','MLE','RMSE'])

        mle_data = pd.DataFrame(mle_data)
        mle_data_i.append(mle_data)

        creek_movern_tributaries_merge_i = creek_movern_df_tributaries.merge(mle_data, left_on = "Tributary", right_on = "test_source_key")

        creek_movern_tributaries_merge[name_mle] = creek_movern_tributaries_merge_i['MLE']
        creek_movern_tributaries_merge[name_rmse] = creek_movern_tributaries_merge_i['RMSE']

        TributariesMLE_i = list(creek_movern_tributaries_merge[name_mle])

        TributariesMLE.append(TributariesMLE_i)

        tributaries_MLE = pd.DataFrame(TributariesMLE)
        tributaries_MLE = tributaries_MLE.transpose()
        tributaries_MLE.rename(columns=lambda x: 'm/n 0.%s' % x, inplace=True)#Name columns

    return tributaries_MLE


#Function to import CHI data for every M/N Value for each Tributary and Main Stem
    
def import_chi_data(path, creek, name):
    
    #Import Data
    creek_movern_df = pd.read_csv((path+name), delimiter=',', header=0, names=['source_key','basin_key','elevation','m_over_n = 0.1','m_over_n = 0.2','m_over_n = 0.3','m_over_n = 0.4','m_over_n = 0.5','m_over_n = 0.6','m_over_n = 0.7','m_over_n = 0.8'])

    creek_movern_df = creek_movern_df.rename(columns={'source_key': 'Tributary'})
    
    return creek_movern_df






#import chi data
chi_data = import_chi_data(path, creek, name)

#seperate into tribs and main stem
chi = chi_data[chi_data['Tributary'] != 0]
chi_ms = chi_data[chi_data['Tributary'] == 0]

#import mle data
tributaries_MLE = create_MLE_data(mn_values = [x / 10.0 for x in range(1, 9, 1)])

#assign bokeh data sources
chi_source = bp.ColumnDataSource(chi)
chi_ms_source = bp.ColumnDataSource(chi_ms)
mle_source = bp.ColumnDataSource(tributaries_MLE)



# Set up plot
plot = figure(plot_height=250, plot_width=500, title="m/n values",x_axis_label='Chi (X)', y_axis_label='Elevation (m)',
              tools="pan,reset,save,wheel_zoom")
plot.circle('x', 'y', source=chi_source)


# Set up widgets
mn_values_slider = Slider(title="m/n values", value=0.0, start=0.1, end=0.8, step=0.1)


# Set up callbacks
def update_data(attrname, old, new):

    # Get the current slider values
    mn = mn_values_slider.value


    # Generate the new curve
    x = chi_source.data['m_over_n = %s' % mn]['chi']
    y = chi_source.data['elevation']

    chi_source.data = dict(x=x, y=y)

for mn in [mn_values]:
    mn.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(mn_values)

curdoc().add_root(column(inputs, plot, width=800))
curdoc().title = "m/n values"









