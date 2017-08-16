import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

creek= "Perkins_creek"
path = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Cache_creek/Previous_LSDTT_version/Channel_extraction/"+creek+"/" #Set path to data
name = "Cache_creek_clip_fullProfileMC_forced_0.5_20_-4924088_20_90_3010.tree" #Set file name

## IMPORT DATA for csv or tree files
#for csv files
#data = np.genfromtxt((path+name), delimiter=',', skip_header=1, names=['id', 'x', 'y', 'chan_number', 'reciever_chan','node_on_reciever_chan', 'node', 'row','column', 'flow_distance', 'chi', 'elevation', 'drainage_area', 'n_data_points', 'm_mean','m_st_dev', 'm_std_err', 'b_mean', 'b_st_dev', 'b_std_err', 'DW_mean', 'DW_st_dev', 'DW_std_err', 'fitted_elev_mean', 'fitted_elev_stdev', 'fitted_elev_std_err'])
#for tree files
data = np.genfromtxt((path+name), delimiter=' ', skip_header=1, names=['chan_number', 'reciever_chan','node_on_reciever_chan', 'node', 'row','column', 'flow_distance', 'chi', 'elevation', 'drainage_area', 'n_data_points', 'm_mean','m_st_dev', 'm_std_err', 'b_mean', 'b_st_dev', 'b_std_err', 'DW_mean', 'DW_st_dev', 'DW_std_err', 'fitted_elev_mean', 'fitted_elev_stdev', 'fitted_elev_std_err'])


def plot_single_channel(data, chan_num):
    plt.figure()
    chan_index = data['chan_number'] == chan_num # 0 = base channel
    chan = data[chan_index] # selects the "True" rows recorded in the boolean index
    flow_distance = chan['flow_distance']-min(chan['flow_distance'])
    elevation = chan['elevation']
    plt.plot(flow_distance, elevation, color='b')
    plt.xlabel('Distance (m)')
    plt.ylabel('Elevation (m)')
    plt.show()
    
def plot_single_channel_chi(data, chan_num):
    chan_index = data['chan_number'] == chan_num
    chan = data[chan_index] # selects the "True" rows recorded in the boolean index
    chi = chan['chi']
    elevation = chan['elevation']
    plt.scatter(chi, elevation, c=chi, cmap=plt.get_cmap("jet"), edgecolors='none')
    plt.xlabel('Chi (X)')
    plt.ylabel('Elevation (m)')
    plt.show()
    
def plot_all_channels(data):
    plt.figure()

    for i in range(0, len(np.unique(data['chan_number']))):
        chan_index = data['chan_number'] == i
        chan = data[chan_index] # selects the "True" rows recorded in the boolean index
        flow_distance = chan['flow_distance']-min(chan['flow_distance'])
        elevation = chan['elevation']
        plt.plot(flow_distance, elevation, color='b')
    plt.xlabel('Distance (m)')
    plt.ylabel('Elevation (m)')
    plt.show()
    
def plot_all_channels_chi(data):
    plt.figure()

    for i in range(0, len(np.unique(data['chan_number']))):
        chan_index = data['chan_number'] == i
        chan = data[chan_index] # selects the "True" rows recorded in the boolean index
        chi = chan['chi']
        elevation = chan['elevation']
        plt.scatter(chi, elevation, c='b', cmap=plt.get_cmap("jet"), edgecolors='none')
    plt.xlabel('Chi (X)')
    plt.ylabel('Elevation (m)')
    plt.title(creek)
    plt.show()

#Example of how to use.
# plt.figure()

# for i in range(0, len(np.unique(data_05['chan_number']))):
#     chan_index = data_05['chan_number'] == i
#     chan = data_05[chan_index] # selects the "True" rows recorded in the boolean index
#     chi = chan['chi']
#     elevation = chan['elevation']
#     plt.scatter(chi, elevation, c=chi, cmap=plt.get_cmap("jet"))
# plt.xlabel('Chi (X)')
# plt.ylabel('Elevation (m)')
# plt.show()