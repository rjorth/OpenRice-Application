from food_search_engine import *
import matplotlib.pyplot as plt 
import sys 
import json 
import numpy as np
import HTMLParser

result = Food_Search_Engine ('openrice_data.json')
result.load_data('openrice_data.json')
a = result.return_filtered_data()
price = []
review =[]
for item in a:
	if item["price-range"] == "Below $50":
	    temp_price = "$0-50"
	    lower_ret, upper_ret = float(temp_price.split("-")[0][1:]), float(temp_price.split("-")[1])
	    price.append((lower_ret + upper_ret)/2) 
	elif item["price-range"] == "Above $801":
	    temp_price = "$801-1000"
	    lower_ret, upper_ret = float(temp_price.split("-")[0][1:]), float(temp_price.split("-")[1])     
	    price.append((lower_ret + upper_ret)/2) 
	else:
	    lower_ret, upper_ret = float(item["price-range"].split("-")[0][1:]), float(item["price-range"].split("-")[1])     
	    price.append((lower_ret + upper_ret)/2)   
for x in a:
	review.append(x['reviews'][0]+ x['reviews'][1] + x['reviews'][2])
ax = plt.gca()
label = ax.set_xlabel("Price", fontsize = 9, labelpad=5)
ax.set_ylabel("Number of reviews", fontsize = 9, labelpad=5)
ax.set_title('The relationship between price and popularity in Hong Kong')
plt.scatter(price,review)
plt.show()