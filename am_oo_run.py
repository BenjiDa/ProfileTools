e = ElevationAnalyzer(file_path,file_name)
e.read_file()
e.set_colors() 

stream_map_properties = {plot_width=600, plot_height=300, title='Title', x_axis_label='Label', y_axis_label='Label'}
stream_map = StreamMap(e)
plot1 = stream_map.create_map()

profile_properties = {'x':'flow_distance','y':'elevation', 'plot_width'=500, 'plot_height':250, 'toolbar_location':'above', 'title':'Title', 'x_axis_label':'Label', 'y_axis_label':'Label'}
profile1 = Profile(e)

profile_properties = {'x':'chi','y':'elevation', 'plot_width'=500, 'plot_height':250, 'toolbar_location':'above', 'title':'Title', 'x_axis_label':'Label', 'y_axis_label':'Label'}
profile2 = Profile(e)


