from am_oo_test import * 
from bokeh.layouts import layout

FILE_NAME = "Mandakini_fullProfileMC_forced_0.45_3_1258909000_10_80_281_for_Arc.csv" #Set file name
FILE_PATH = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Test_data/" #Set path to data

stream_map_properties = {'title':'Stream Map', 'x_axis_label':'Easting', 'y_axis_label':'Northing'}

stream_map = StreamMap(file_path=FILE_PATH,file_name=FILE_NAME,color_variable='elevation')
stream_map.set_properties(stream_map_properties)
plot1 = stream_map.create_stream_map()




profile_properties_flow_distance = {'x':'flow_distance', 
												 'y':'elevation',
												'title':'Flow Distance v Elevation Profile', 
												'x_axis_label':'Flow Distance', 
												'y_axis_label':'Elevation'}

profile1 = Profile(file_path=FILE_PATH,file_name=FILE_NAME,color_variable='elevation')
profile1.set_properties(profile_properties_flow_distance)
plot2 = profile1.create_profile()

profile_properties_chi = {'x':'chi', 
							'y':'elevation',
							'title':'Chi Profile', 
							'x_axis_label':'Chi', 
							'y_axis_label':'Elevation'}
profile2 = Profile(file_path=FILE_PATH,file_name=FILE_NAME,color_variable='elevation')
profile2.set_properties(profile_properties_chi)
plot3 = profile2.create_profile()

out = layout([plot1], [plot2], [plot3])
bp.show(out)


