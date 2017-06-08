from am_oo_test import *
import unittest 
import pdb 

FILE_NAME = "Mandakini_fullProfileMC_forced_0.45_3_1258909000_10_80_281_for_Arc.csv" #Set file name
FILE_PATH = "/Users/bmelosh/VagrantBoxes/LSDTopoTools/Topographic_projects/Test_data/" #Set path to data


class TestElevationAnalyzer(unittest.TestCase):

	def setUp(self):
		self.elevation_analyzer = ElevationAnalyzer(file_path=FILE_PATH,file_name=FILE_NAME,color_variable='elevation')

	def test_elevation_analyzer_initializes_properly(self):
		self.assertEqual(self.elevation_analyzer.file_name, FILE_NAME)
		self.assertEqual(self.elevation_analyzer.file_path, FILE_PATH)
		self.assertEqual(self.elevation_analyzer.color_variable, 'elevation')


	def test_read_file(self):
		self.elevation_analyzer.read_file()
		first_data_cell = self.elevation_analyzer.source.data['DW_mean'][0]
		first_df_node = self.elevation_analyzer.df['node'][0]
		self.assertEqual(first_data_cell, 0)
		self.assertEqual(first_df_node, 133864)

	def test_set_colors(self):
		self.elevation_analyzer.read_file()
		self.elevation_analyzer.set_colors()
		first_color = self.elevation_analyzer.source.data['colors'][0]
		self.assertEqual(first_color, '#7f0000')


class TestStreamMap(unittest.TestCase):
	def setUp(self):
		self.stream_map_properties = {'title':'Stream Map', 'x_axis_label':'Easting', 'y_axis_label':'Northing'}


	def test_stream_map_initializes_properly(self):
		self.stream_map = StreamMap(file_path=FILE_PATH,file_name=FILE_NAME,color_variable='elevation')

		self.assertEqual(self.stream_map.file_name, FILE_NAME)
		self.assertEqual(self.stream_map.file_path, FILE_PATH)
		self.assertEqual(self.stream_map.color_variable, 'elevation')
		self.assertEqual(self.stream_map.x, 'x')

	def test_stream_map_sets_custom_properties(self):


		self.stream_map = StreamMap(file_path=FILE_PATH,file_name=FILE_NAME,color_variable='elevation')
		self.stream_map.set_properties(self.stream_map_properties)

		self.assertEqual(self.stream_map.title, 'Stream Map')
		self.assertEqual(self.stream_map.x_axis_label, 'Easting')

	def test_plotting_stream_map(self):
		self.stream_map = StreamMap(file_path=FILE_PATH,file_name=FILE_NAME,color_variable='elevation')
		self.stream_map.set_properties(self.stream_map_properties)
		self.stream_map.create_stream_map()


class TestProfile(unittest.TestCase):
	def setUp(self):
		self.profile_properties_flow_distance = {'x':'flow_distance', 
												 'y':'elevation',
												'title':'Flow Distance v Elevation Profile', 
												'x_axis_label':'Easting', 
												'y_axis_label':'Northing'}

	def test_create_profile(self):
		self.profile = Profile(file_path=FILE_PATH,file_name=FILE_NAME,color_variable='elevation')
		self.profile.set_properties(self.profile_properties_flow_distance)
		self.profile.create_profile()






