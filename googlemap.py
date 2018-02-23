
import gmplot
from food_search_engine import *
result = Food_Search_Engine ('openrice_data.json')
result.load_data('openrice_data.json')
result.filter({'cuisine' : ['Japanese']}) 
a = result.return_filtered_data()
lat = []
lng = []

for item in a :
	lat.append(item['address'][0])

for item in a :
	lng.append(item['address'][1])


gmap = gmplot.GoogleMapPlotter(22.325222,114.1664163,12)


gmap.heatmap(lat,lng,opacity=1, gradient=0 )

gmap.draw("googlemap.html")