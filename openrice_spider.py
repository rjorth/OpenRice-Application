import scrapy
import json
import re 
import os 
import sys 
sys.stdout = open("otput_spider.txt", "w")
class OpenriceSpider(scrapy.Spider):
	name = 'openrice'
	allowed_domains = ['www.openrice.com']
	

	def start_requests(self):
		headers = {
			'accept-encoding': 'gzip, deflate, sdch, br',
			'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'cache-control': 'max-age=0',
		}
		file = open('openrice_urls.txt', 'r')
		for line in file:
		# first_line = file.readline()
			yield scrapy.Request(url= str(line)[:-1], headers=headers, callback=self.parse)
		# output_filename = 'openrice_data.json' 
		# with open(output_filename, 'a') as file: # you should delete the intermediate file before you run the code
		# 	json.dump([], file, indent = 2)
		# 	file.close()

	def parse(self, response):	
		data = {} # it stores all necessary information of a restaurant 
		restaurant_data = str(response.xpath('//*[@id="global-container"]/main/script[1]/text()').extract()) 
		restaurant_review = response.css("div.score-div::text").extract()
		review = []
		for x in restaurant_review:
			review.append(int(x.encode('utf-8')))  
		name = str(re.findall('name.+?,',restaurant_data))[10:-4]
		price_range = str(re.findall('priceRange.+?,',restaurant_data))[16:-4]
		district = str(re.findall('addressLocality.+?,',restaurant_data)) [21:-4]
		latitude = str(re.findall('latitude.+?,',restaurant_data))[13:-3]
		longitude = str(re.findall('longitude.+?r',restaurant_data))[14:-5]
		address = [float(latitude), float(longitude)]
		cuisine_data = str(response.xpath('/html/head/meta[8]').extract())
		cuisine_total = str(re.findall ('content.+\|',cuisine_data)) [11:-3]
		cuisine =  cuisine_total.split("|")
		url = str(re.findall('url".+?,',restaurant_data))[9:-4]
		rating = str(response.css('div.header-score::text').extract())[3:-2] 
		data["name"] = name 
		data["cuisine"] = cuisine
		data["address"] = address
		data['rating'] = float(rating) 
		data['reviews'] = review 
		data['district'] = district
		data['url'] = url 
		data['price-range'] = price_range
		output_filename = '11openrice_data.json'  
		with open(output_filename, 'a') as file: # you should delete the intermediate file before you run the code
			json.dump([data], file, indent = 2)
			file.close()
		f = open(output_filename,'r')
		old_data = f.read()
		f.close()
		new_data = old_data.replace("][", ",") 
		f = open('openrice_data_new.json','w')
		f.write(new_data)
		f.close()
		os.remove('openrice_data.json')
		os.rename('openrice_data_new.json', 'openrice_data.json')
		
			

		