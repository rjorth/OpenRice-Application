from food_search_engine import *
import matplotlib.pyplot as plt 
import sys 
import json 
import numpy as np
import HTMLParser
from collections import OrderedDict
#sys.stdout = open("top_10_reviewed.txt", "w")

result = Food_Search_Engine ('openrice_data.json')
result.load_data('openrice_data.json')
result.filter({'district' : ['Mong Kok']}) 
a = result.return_filtered_data()

cuisine = []
result = {}
for item in a:
	cuisine.append(item['cuisine'][0])
for item in cuisine:
	if item in result:
		result[item] += 1
	else: 
		result[item] = 1
#print result
sort_result = []
for x, y in result.items():
	sort_result.append([y ,x])
sort_result.sort(reverse = True)
plot_result_num = []
plot_result_label = []
other_num = 0
for item in sort_result[0:5]:
 	plot_result_num.append(item[0])
 	plot_result_label.append(item[1])

for item in sort_result[5::]:
	other_num = other_num + item[0]

plot_result_num.append(other_num)
plot_result_label.append("others")


plt.pie(plot_result_num,  labels=plot_result_label, autopct='%1.1f%%',
         startangle=90)
ax = plt.gca()
ax.set_title("Top-5 cuisine types in Mong Kok")

plt.show()

