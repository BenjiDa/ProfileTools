

#playing with Pandas to plot data, trying to split individual channels.


# grid_fp = '/Users/bmelosh/projects/LSDTopoTools/MandakiniSHP/MandakiniSHP.shp'
# grid = gpd.read_file(grid_fp)

# import pandas as pd

# data = pd.read_csv((path))

# df = pd.DataFrame(data)

# unique_channels = df.channel_number.unique() #display different channels
# print(len(unique_channels))

# a = df.loc[df['channel_number'] == 0]
# b = df.loc[df['channel_number'] == 1]
# c = df.loc[df['channel_number'] == 2]
# d = df.loc[df['channel_number'] == 3]
# e = df.loc[df['channel_number'] == 4]

# grouped = df.groupby('channel_number')

# #for loop for dividing up the channel data
# # b = []
# # for i in range(0, len(unique_channels)): 
# #     a = df.loc[df['channel_number'] == i]
# #     a.
# grouped['elevation'].mean()


# # for i, group in grouped:
# #     #plt.figure()
# #     group.plot(x='x', y='y', title=str(i))


#Dealing with projections
# from pyproj import transform, Proj
# import numpy as np
# from bokeh.models.ranges import Range1d

# #input_proj = Proj(init='epsg:4326') #geographic
# #output_proj = Proj(init='epsg:3857') #web mercator
# input_proj = Proj(init='epsg:32644')
# output_proj = Proj(init='epsg:32644') 

# xmin_lng = 280000 #-139 #
# #, 3350000 (bottom left) 345000, 3410000 (top right)
# xmax_lng = 345000#-50

# ymin_lat = 3350000#20

# ymax_lat = 3410000 #55


# xmin_meters, ymin_meters = transform(input_proj, output_proj, xmin_lng, ymin_lat)
# xmax_meters, ymax_meters = transform(input_proj, output_proj, xmax_lng, ymax_lat)

# #reporjecting can be vectorized
# x_longitudes = np.array([280000, 345000])
# y_latitudes = np.array([3350000, 3410000])
# x_meters, y_meters = transform(input_proj, output_proj, x_longitudes, y_latitudes)

# #Bokeh 1D Ranges 
# x_range = Range1d(*x_meters)
# y_range = Range1d(*y_meters)

# print(x_meters)
# print(x_range)
# print(xmin_lng, xmin_meters)









