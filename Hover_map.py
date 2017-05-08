#use bokeh to plot map of x,y stream data and have interactive hover showing elevation and chi.

from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, BoxSelectTool
from datashader.colors import inferno

#set output type
# output_notebook()

#Call all data into pandas
pdata = pd.read_csv((path))
#pdata['geometry'] = pdata.apply(lambda z: Point(z.x, z.y), axis=1)\n",
#geo_pdata = gpd.GeoDataFrame(read_pdata)

#Define a source for all the data into a Bokeh ColumnDataSource
source = ColumnDataSource(pdata)

#start the figure
p = figure(title="Stream channel elevation map")


#visualize map
#color_mapper = LogColorMapper(palette=palette)

# Plot grid\n",
#p.patches(pdata['x'], pdata['y'], source=source,
#    fill_color={'field': 'elevation', 'transform': color_mapper},
#    fill_alpha=1.0, line_color="black", line_width=0.05)

p.circle(pdata['x'], pdata['y'], source=source, color='red', size=6)

#setting interactive plot
my_hover = HoverTool()
my_hover.tooltips = [('Elevation (m)', '@elevation'), ('Chi (X)', '@chi')]
p.add_tools(my_hover)

show(p)
# #Output filepath
# outfp = "/Users/bmelosh/projects/LSDTopoTools/profile_tool.html"
# save(p, outfp)