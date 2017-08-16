import gdal
import matplotlib.pyplot as plt
import raster_plot


#Use Matplotlib to plot raster as well as stream profile and chi profile

raster_path = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Cache_creek/"
raster = gdal.Open(raster_path + "/Cache_creek_clip.bil")#Get raster data
dem = raster.ReadAsArray()

cm = plt.cm.gist_earth


fig, ax = plt.subplots(3, figsize=(10,10), sharex=False) #define 2 subfigures

ax[0].contourf(X, Y, dem, levels=np.linspace(np.amin(dem[dem > 0]),np.amax(dem), 50))
ax[0].plot(data['x'], data['y'], 'ro',  markersize=2)
#ax[0].imshow(fA, interpolation='nearest', vmin=0, cmap=plt.cm.gray) 
ax[0].set_aspect('equal')
ax[0].set_title('Terrain map with stream channel')
ax[0].set_ylabel('Northing')
ax[0].set_xlabel('Easting')


ax[1].scatter(data['flow_distance'], data['elevation'], c=data['elevation'], cmap=cm)
ax[1].set_title('Stream Map')
ax[1].set_ylabel('Elevation (m)')
ax[1].set_xlabel('Distance (m)')


ax[2].scatter(data['chi'], data['elevation'], c=data['elevation'], cmap=plt.get_cmap("jet"))
ax[2].text(3, 2500, 'm/n = 0.45')
ax[2].set_ylabel('Elevation (m)')
ax[2].set_xlabel('Chi (X)')


plt.show()