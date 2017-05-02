#This script plots an interactive digital elevation model in bokeh, the output is an .html file


import pandas as pd
import geopandas as gpd
from bokeh.models import HoverTool
from bokeh.palettes import RdYlBu11 as palette
from bokeh.models import LogColorMapper
import pysal as ps




grid_fp = '/Users/bmelosh/projects/LSDTopoTools/MandakiniSHP.shp' #enter your path to shapefile here
grid = gpd.read_file(grid_fp)


# output to static HTML file, name your output file here.
output_file("Interactive_topo.html")


#Dealing with data projection, don't need this now but might in the future
# CRS = grid.crs
# print(CRS)
#convert data to a specific projection
#points['geometry'] = points['geometry'].to_crs(crs=CRS)


def getPolyCoords(row, geom, coord_type):
    """Returns the coordinates ('x' or 'y') of edges of a Polygon exterior"""

    # Parse the exterior of the coordinate
    exterior = row[geom].exterior

    if coord_type == 'x':
        # Get the x coordinates of the exterior
        return list( exterior.coords.xy[0] )
    elif coord_type == 'y':
        # Get the y coordinates of the exterior
        return list( exterior.coords.xy[1] )
    
grid['x'] = grid.apply(getPolyCoords, geom='geometry', coord_type='x', axis=1)
grid['y'] = grid.apply(getPolyCoords, geom='geometry', coord_type='y', axis=1)



## Define classificiations for plotting
#set the name of Elevation here. e.g.  grid['elevation']
mini = min(grid['DN'])
maxi = max(grid['DN'])
breaks = [x for x in range(mini, maxi, 50)]

# Initialize the classifier and apply it
classifier = ps.User_Defined.make(bins=breaks)
elev_classif = grid[['DN']].apply(classifier)

# Rename the classified column
elev_classif.columns = ['DN_Class']

# Join it back to the grid layer
grid = grid.join(elev_classif)


# Make a copy, drop the geometry column and create ColumnDataSource
g_df = grid.drop('geometry', axis=1).copy()
gsource = ColumnDataSource(g_df)

# Create the color mapper
color_mapper = LogColorMapper(palette=palette)




# Initialize our figure
p = figure(title="Elevations")

#setting interactive plot
my_hover = HoverTool()
my_hover.tooltips = [('Elevation (m)', '@DN')]
p.add_tools(my_hover)

# Plot grid
p.patches('x', 'y', source=gsource,
         fill_color={'field': 'DN_Class', 'transform': color_mapper},
         fill_alpha=1.0, line_color="black", line_width=0.05)



show(p)
