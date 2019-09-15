import pandas as pd
import requests
from pprint import pprint
import time

class BurguiClass(object):

	def __init__(self):
		self.burgui_var = "love"
	#returns a list of coordinates from a given file
	def coord_list(self, file_name):
		df = pd.read_excel(file_name, sheet_name = 0)
		lat_list = df['Latitude'].tolist()
		long_list = df['Longitude'].tolist()
		return list(zip(lat_list, long_list))
	#returns a list of geolocs from a given file
	def get_geoloc_list(self, file_name):
		df = pd.read_excel(file_name, sheet_name = 0)
		geoloc_list = df['CompanyNumber'].tolist()
		return geoloc_list
	#takes a a list of geolocs and a list of coordinates and returns the forecast
	def get_forecast(self, geoloc_list, coordinates_list):
		for coordinate_pair in coordinates_list:
			url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=bab23a0c45a4ba58df288fb05a6f7323'.format(coordinate_pair[0], coordinate_pair[1])
			#gets the data from openweathermap
			data = requests.get(url).json()
			time.sleep(0.3)
			#adds 0 to missing or empty 'rain'
			for reading in data['list']:
				if 'rain' not in reading:
					reading['rain'] = {'3h': 0}
				elif reading['rain'] == {}:
					reading['rain'] = {'3h': 0}
			#fills the list of inches of rain
			rain_amounts_list = [reading['rain']['3h'] for reading in data['list']]
		#creates the lists to display in the dataframe	
		rain_amounts = [rain for coordinate_pair in coordinates_list for rain in rain_amounts_list]
		dates = [date for coordinate_pair in coordinates_list for date in [reading['dt_txt'] for reading in data['list']]]
		geolocs = [geoloc for rain in rain_amounts_list for geoloc in geoloc_list]
		#creates the dataframe
		df = pd.DataFrame({'Geoloc': geolocs, 'Date': dates, 'Rain (inches)': rain_amounts})
		return df
	def main(self):
		excel_file = input('File Name: ')
		list_of_geolocs = self.get_geoloc_list(excel_file)
		list_of_coords = self.coord_list(excel_file)
		forecast = self.get_forecast(list_of_geolocs, list_of_coords)
###Not sure if it needs to print or return###
		return forecast

bcrunner = BurguiClass()

print(bcrunner.main())
