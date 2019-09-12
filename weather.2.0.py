def coord_list(file_name):
	import pandas as pd
	df = pd.read_excel(file_name, sheet_name = 0)
	lat_list = df['Latitude'].tolist()
	long_list = df['Longitude'].tolist()
	return list(zip(lat_list, long_list))

def get_forecast(coordinates_list): #takes a list of coordinates and returns the forecast
	import requests
	from pprint import pprint
	import pandas as pd
	#initiantes lists
	dates = []
	rain_amounts = []
	coordinates = []
	for coordinate_pair in coordinates_list:
		url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=bab23a0c45a4ba58df288fb05a6f7323'.format(coordinate_pair[0], coordinate_pair[1])
		#gets the data from openweathermap
		data = requests.get(url).json()
		#creates a list of date/time
		dates_list = [reading['dt_txt'] for reading in data['list']]
		for date in dates_list:
			dates.append(date)
		#adds 0 to missing or empty 'rain'
		for reading in data['list']:
			if 'rain' not in reading:
				reading['rain'] = {'3h': 0}
			elif reading['rain'] == {}:
				reading['rain'] = {'3h': 0}
		#creates a list of inches of rain	
		rain_amounts_list = [reading['rain']['3h'] for reading in data['list']]
		for rain in rain_amounts_list:
			rain_amounts.append(rain)
		#creates list of coordinates	
		for rain in rain_amounts_list:
			coordinates.append(coordinate_pair)
	#creates the dataframe
	df = pd.DataFrame({'Coordinates': coordinates, 'Date': dates, 'Rain (inches)': rain_amounts})
	return df

excel_file = input('File Name: ')
list_of_coords = coord_list(excel_file)
forecast = get_forecast(list_of_coords)

print(forecast)
