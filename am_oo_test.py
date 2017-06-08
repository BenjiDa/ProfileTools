from bokeh.models import ColumnDataSource, DataRange1d
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm
import bokeh.plotting as bp
from bokeh.models import HoverTool


class ElevationAnalyzer():
    def __init__(self, file_path, file_name, color_variable):
        self.file_path = file_path
        self.file_name = file_name
        self.source = None
        self.df = None 
        self.color_variable = color_variable
        self.read_file()
        self.set_colors()


    def read_file(self):
        df = pd.read_csv(self.file_path+self.file_name)
        source = ColumnDataSource(df) #Define the data source in bokeh
        self.source = source 
        self.df = df 

    def set_colors(self):
        colors = ["#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in 255*mpl.cm.jet(mpl.colors.Normalize()(self.source.data[self.color_variable]))]
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
    def __init__(self, file_path,file_name,color_variable):
        # look up syntax for this
    
        ElevationAnalyzer.__init__(self,file_path, file_name, color_variable)
        self.x = 'x'
        self.y = 'y'
        self.plot_width = 600
        self.plot_height = 300


    def set_properties(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


    def create_stream_map(self): 
        x_range, y_range = self.define_boundaries()
        plot = bp.figure(plot_width=self.plot_width, plot_height=self.plot_height, x_range=x_range, y_range=y_range, title=self.title, x_axis_label=self.x_axis_label, y_axis_label=self.y_axis_label)
        cr = plot.circle(x=self.x, y=self.y, size=20,
                         fill_color="grey", hover_fill_color="firebrick",
                         fill_alpha=0.03, hover_alpha=0.3,
                         line_color=None, hover_line_color="white", source=self.source)
        plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
        plot.circle(x='x', y='y', size=2, color='colors', source=self.source)
        return plot

class Profile(ElevationAnalyzer):
    def __init__(self, file_path,file_name,color_variable):
        # look up syntax for this
        ElevationAnalyzer.__init__(self, file_path, file_name, color_variable)
        self.plot_width=500
        self.plot_height=250

    def set_properties(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def create_profile(self):
        elev_range = self.define_elevation_boundaries()
 
        plot = bp.figure(plot_width=500, plot_height=250, toolbar_location='above', 
                         title=self.title, x_axis_label=self.x_axis_label, y_axis_label=self.y_axis_label, y_range=elev_range)

        cr = plot.circle(x=self.x, y=self.y, size=20,
                         fill_color='grey', hover_fill_color="firebrick",
                         fill_alpha=0.03, hover_alpha=0.3,
                         line_color=None, hover_line_color="white", source=self.source)
        plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
        plot.circle(x=self.x, y=self.y, size=2, color='colors', source=self.source) 
        return plot





