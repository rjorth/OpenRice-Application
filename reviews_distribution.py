from food_search_engine import *
import matplotlib.pyplot as plt 
import sys 
import json 
import numpy as np
import HTMLParser

result = Food_Search_Engine ('openrice_data.json')
result.load_data('openrice_data.json')
result.filter({'district' : ['Tsim Sha Tsui']}) 
a = result.return_filtered_data()


review =[]

for x in a:
	review.append(x['reviews'][0]+ x['reviews'][1] + x['reviews'][2])
ax = plt.gca()
ax.set_xlabel('Number of reviews', fontsize = 9, labelpad=5)
ax.set_ylabel('Number of restaurants', fontsize = 9, labelpad=5)
ax.set_title("The Distribution of the number of reviews in Tsim Sha Tsui")
plt.hist(review)
plt.show()