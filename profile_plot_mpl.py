import matplotlib.pyplot as plt

#Use Matplotlib to plot raster as well as stream profile and chi profile

#Create arrays for plotting raster with matplotlib
#X, Y, array_part= raster_subsample_xy_generator(raster, creek_data_df)

#Set up the figure and subplots
fig = plt.figure(figsize=(15,15))
fig.subplots_adjust(hspace=0.5)
ax1 = plt.subplot2grid((4, 1), (0, 0), colspan=2, rowspan=2)
ax2 = plt.subplot2grid((4, 1), (2, 0))
ax3 = plt.subplot2grid((4, 1), (3, 0))

#cm = plt.cm.gist_earth #set colormap

ax1.contourf(X, Y, array_part, levels=np.linspace(np.amin(array_part[array_part > 0]),np.amax(array_part), 50))
ax1.plot(creek_data_df['x'], creek_data_df['y'], 'ro',  markersize=1, markeredgewidth=0.0)
ax1.set_aspect('equal')
ax1.set_title('Terrain map with stream channel')
ax1.set_ylabel('Northing')
ax1.set_xlabel('Easting')


ax2.scatter(creek_data_df['distance'], creek_data_df['elevation'], c=creek_data_df['m_chi'], cmap=plt.get_cmap("coolwarm"), s = 4, edgecolors='none')#, viridis, plasma
ax2.set_xlabel('Distance (m)')
ax2.set_ylabel('Elevation (m)')
ax2.set_title(creek)

ax3.scatter(creek_data_df['chi'], creek_data_df['elevation'], c=creek_data_df['m_chi'], cmap=plt.get_cmap("coolwarm"), s = 4, edgecolors='none')#, viridis, plasma
ax3.set_xlabel('Chi')
ax3.set_ylabel('Elevation (m)')
ax3.set_title(creek)


plt.show(fig)