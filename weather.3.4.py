import pandas as pd
import requests
from pprint import pprint
import time
from datetime import datetime
from dateutil import tz

class BurguiClass(object):

	def __init__(self):
		self.burgui_var = "love"
	#returns a list of coordinates from a given file
	def get_coord_list(self, file_name):
		df = pd.read_excel(file_name, sheet_name = 0)
		coord_list = list(zip(df['Latitude'].tolist(), df['Longitude'].tolist()))
		return coord_list
	#returns a list of geolocs from a given file
	def get_geoloc_list(self, file_name):
		df = pd.read_excel(file_name, sheet_name = 0)
		geoloc_list = df['CompanyNumber'].tolist()
		return geoloc_list
	#takes a list of geolocs and a list of coordinates and returns the forecast
	def get_forecast(self, geoloc_list, coordinates_list):
		rain_amounts_list = []
		date_time = []
		geolocs = []
		n = 0
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
			#creates a list of inches of rain
			rain_amounts_list.extend([round(float(reading['rain']['3h'])*0.0393701, 2) for reading in data['list']])
			date_time.extend([date.split(' ') for date in [reading['dt_txt'] for reading in data['list']]])
			geolocs.extend(geoloc_list[n] for reading in data['list'])
			n += 1
		#creates the lists to display in the dataframe
		dates = [date[0] for date in date_time]
		from_zone = tz.gettz('UTC')#this is use to convert from UTC to EST
		to_zone = tz.gettz('America/New_York')#this is use to convert from UTC to EST
		times = [datetime.strftime(datetime.strptime(time[1], '%H:%M:%S').replace(tzinfo=from_zone).astimezone(to_zone), '%H:%M:%S') for time in date_time]#creates the list of times and converts the time from UTC to EST
		#creates the dataframe
		df = pd.DataFrame({'Geoloc': geolocs, 'Date': dates, 'Time': times, 'Inches': rain_amounts_list})
		return df

	def main(self):
		excel_file = input('File Name: ')
		list_of_geolocs = self.get_geoloc_list(excel_file)
		list_of_coords = self.get_coord_list(excel_file)
		forecast = self.get_forecast(list_of_geolocs, list_of_coords)
		return forecast

bcrunner = BurguiClass()

rain_forecast = bcrunner.main()

print(rain_forecast)

rain_forecast.to_excel('{}.xlsx'.format(datetime.now()))