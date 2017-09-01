import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

#Function to import MLE data and create a dataframe with MLE data for all TRIBUTARIES for each M/N Value

#Create a function to pull in MLE data
mn_values = [x / 10.0 for x in range(1, 9, 1)]#create a list of floats.


def group_chi_mle_data(creek, path, fname, mn_values):
    #Import Chi Data
    movern_df = pd.read_csv((path+fname), delimiter=',', header=0, names=['source_key','basin_key','elevation','m_over_n = 0.1','m_over_n = 0.2','m_over_n = 0.3','m_over_n = 0.4','m_over_n = 0.5','m_over_n = 0.6','m_over_n = 0.7','m_over_n = 0.8'])
    movern_df = movern_df.rename(columns={'source_key': 'Tributary'})
    movern_df_tribs = movern_df[movern_df['Tributary']!=0]
    movern_df_ms = movern_df[movern_df['Tributary']==0]

    #import MLE Data and merge with Chi
    mle_data_i = []
    mle_data_merge = pd.DataFrame()
    for mn in mn_values:

        movern_df = pd.read_csv((path+fname), delimiter=',', header=0, names=['source_key','basin_key','elevation','m_over_n = 0.1','m_over_n = 0.2','m_over_n = 0.3','m_over_n = 0.4','m_over_n = 0.5','m_over_n = 0.6','m_over_n = 0.7','m_over_n = 0.8'])
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

    return movern_df_tribs_merge, movern_df_ms, mle_data_merge


def color_maker(tribs, mn, colormap='autumn_r'):
    
    s = tribs.groupby(by='MLE m/n %s' % mn).size()
    cmap = list(s.index.values)
    color_index = pd.Series([cmap.index(item) for item in tribs['MLE m/n %s' % mn].values])
    norm = mpl.colors.Normalize()
    norm.autoscale(color_index)
    sm = mpl.cm.ScalarMappable(norm, colormap)#Wistia autumn_r

    colors = [
        "#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, a in [sm.to_rgba(item, bytes=True) for item in color_index]
    ]

    return colors



