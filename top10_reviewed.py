from food_search_engine import *
import matplotlib.pyplot as plt 
import sys 
import json 
import numpy as np
import HTMLParser
HTMLParser.HTMLParser().unescape('&#233;')
parser = HTMLParser.HTMLParser()
# sys.stdout = open("top_10_reviewed.txt", "w")

result = Food_Search_Engine ('openrice_data.json')
result.load_data('openrice_data.json')
result.filter({'district' : ['Sha Tin']}) 
a = result.return_filtered_data()


restaurant = []
review =[]
result = []
for item in a:
	restaurant.append(item['name'])
for x in a:
	review.append(x['reviews'][0]+ x['reviews'][1] + x['reviews'][2])

for i in range (0, len(restaurant)):
	result.append([review[i] , restaurant[i]])

restaurant = []
review =[]
result.sort(reverse = True)
for element in  result:
	restaurant.append(element[1]) 
	review.append(element[0]) 
x_value = np.arange(10,0,-1)

restaurant_decode =[]
for x in restaurant[0:10]:
	restaurant_decode.append(parser.unescape(x))
#abc = plt.subplots()
#plt.figure()
plt.barh(x_value, review[0:10], facecolor = 'blue')
ax = plt.gca()
label = ax.set_xlabel('Number of reviews', fontsize = 9, labelpad=5)
#plt.xticks(())
plt.yticks(x_value, restaurant_decode,fontsize = 9)
rects = ax.patches

ax.set_title("Top-10 most reviewed restaurants in Sha TIn")


for i, v in enumerate(review[0:10][::-1]):
    ax.text(v+1 , i + 0.8, str(v), color='blue', fontweight='bold')
plt.show()

