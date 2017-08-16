from bokeh.models import ColumnDataSource
import pandas as pd


class ElevationAnalyzer():
	def init(self, file_path, file_name, *kwargs):
		self.file_path = file_path
		self.file_name = file_name
		self.source = None
		self.df = None 


	def read_file(self):
		df = pd.read_csv(self.file_path+self.file_name)
		source = ColumnDataSource(df) #Define the data source in bokeh
		self.source = source 
		self.df = df 

	def set_colors(self):
		colors = color_by_variable('elevation', self.source)
		self.source.data['colors']= colors #add a new coloumn to the source dataset to pass into color plot

	def define_boundaries(self,r=1000):
	    xmin = self.df['x'].min()
	    xmax = self.df['x'].max()
	    ymin =self.df['y'].min()
	    ymax = self.df['y'].max()
	    x_range = (xmin-r, xmax+r)
	    y_range = (ymin-r, ymax+r)	
	    return x_range, y_range 

	#define elevation boundaries for profile plots to use for interactive zooming
	def define_elevation_boundaries(self,r=1000):
	    zmin=min(self.source.data['elevation'])
	    zmax=max(self.source.data['elevation'])
	    elevation_range = DataRange1d(bounds=(zmin-r, zmax+r))
	    return elevation_range


class StreamMap(ElevationAnalyzer): 
	def init(self, **kwargs):
		# look up syntax for this
		super.ElevationAnalyzer()
		self.x = 'x'
		self.y = 'y'

	def create_stream_map(self): 
		x_range, y_range = self.define_boundaries()

	    plot = bp.figure(plot_width=plot_width, plot_height=plot_height,x_range=x_range, y_range=y_range, title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
	    cr = plot.circle(x=self.x, y=self.y, size=20,
	                     fill_color="grey", hover_fill_color="firebrick",
	                     fill_alpha=0.03, hover_alpha=0.3,
	                     line_color=None, hover_line_color="white", source=e.source)
	    plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
	    plot.circle(x='x', y='y', size=2, color='colors', source=e.source)
	    return plot

class Profile(ElevationAnalyzer):
	def init(self, **kwargs):
		# look up syntax for this
		super.ElevationAnalyzer()

	def profile(elev_range, source, x='x', y='y', plot_width=500, plot_height=250, toolbar_location='above', title='Title', x_axis_label='Label', y_axis_label='Label'):
    	elev_range = self.define_elevation_boundaries()
 
		plot = bp.figure(plot_width=500, plot_height=250, toolbar_location='above', 
		                 title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label, y_range=elev_range)

		cr = plot.circle(x=x, y=y, size=20,
		                 fill_color='grey', hover_fill_color="firebrick",
		                 fill_alpha=0.03, hover_alpha=0.3,
		                 line_color=None, hover_line_color="white", source=source)
		plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
		plot.circle(x=x, y=y, size=2, color='colors', source=source) 
		return plot





