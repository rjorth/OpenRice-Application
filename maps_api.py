import gmplot
import requests
from food_search_engine import *
import json
import sys 
import os 
#sys.stdout = open("output_maps_api.txt", "w")

result = Food_Search_Engine ('openrice_data.json')
result.load_data('openrice_data.json')
result.filter({'district' : ['Sha Tin']}) 
a = result.return_filtered_data()
#load the data and initialize the values
coordinate =[]
for item in a:
	coordinate.append(item['address'])


coordinate_string = ""
for item in coordinate:
	coordinate_string = coordinate_string + str(item[0]) + "," + str(item[1]) + "|"


for item in coordinate:
	key = "AIzaSyBXK-eO4ZJ3xuI65TVLmgpI1Zz-Vuy0uoU"
	query = 'origins=22.4179252,114.2027235&destinations='+ str(item[0]) +',' +str(item[1]) + '&key=' + key + '&mode=transit&departure_time=1512102900'


	url = "https://maps.googleapis.com/maps/api/distancematrix/json?" + query
	
	res = requests.get(url).json()

	with open("travel_time.json", 'a') as file: # you should delete the intermediate file before you run the code
		json.dump([res], file, indent = 2)
		file.close()
		f = open("travel_time.json",'r')
		old_data = f.read()
		f.close()
		new_data = old_data.replace("][", ",") 
		f = open('travel_time_new.json','w')
		f.write(new_data)
		f.close()
		os.remove('travel_time.json')
		os.rename('travel_time_new.json', 'travel_time.json')

with open('travel_time.json') as json_data:
	google_data = json.load(json_data)	

result = []
#print len(coordinate), len(google_data)
for i in range (0, len(coordinate)):
	result.append([coordinate[i],google_data[i]])

result_blue = []
result_red = []
for item in result:
	 #result_1.append(item[1]["rows"][0]["elements"][0])
	 if item[1]["rows"][0]["elements"][0]["status"] == "ZERO_RESULTS":
	 	result.remove(item)


for item in result: 
	if item[1]["rows"][0]["elements"][0]["duration"]['value'] > 3600 :
		result.remove(item)

for item in result: 
	if item[1]["rows"][0]["elements"][0]["duration"]['value'] <= 2100 :
		result_blue.append(item)

	elif item[1]["rows"][0]["elements"][0]["duration"]['value'] >2100 & item[1]["rows"][0]["elements"][0]["duration"]['value'] <=3600:
	 	result_red.append(item)
	else:
	 	print "shouldn't get here"

gmap = gmplot.GoogleMapPlotter(22.395607,114.1963153,13)

blue_lat = []
blue_log = []
red_lat = []
red_log = []

for item in result_blue:
	blue_lat.append(item[0][0])
	blue_log.append(item[0][1])

for item in result_red:
	red_lat.append(item[0][0])
	red_log.append(item[0][1])

gmap.scatter(blue_lat, blue_log, 'blue', size=40, marker=False)
gmap.scatter(red_lat, red_log, 'red', size=40, marker=False)
# gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
# gmap.heatmap(heat_lats, heat_lngs)

gmap.draw("maps_api.html")


 
