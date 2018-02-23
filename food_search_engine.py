import json
import sys 
import math 
import numpy as np 
sys.stdout = open("output_food_search_engine.txt", "w")

class Food_Search_Engine:
    # original data from crawled json file
    original_data = []
    # the result after filter/ranking
    query_result = []


    def __init__(self, json_file_name):
        self.load_data(json_file_name)
        self.reset()

    def load_data(self, json_file_name):
        with open(json_file_name) as json_data:
            self.original_data = json.load(json_data)

    def reset(self):
        self.query_result = self.original_data

    def filter(self, filter_cond):
        result = self.query_result
        
        for k, v in filter_cond.items():
            if k == "name":     
                tem_list = []
                for ret in result:
                    for item in v:
                        if item == ret[k]:
                            tem_list.append(ret)
                result = [d for d in result if d in tem_list]
    
        for k, v in filter_cond.items():            
            if k == "cuisine": 
                tem_list = []    
                for ret in result:
                    for dish in ret[k]:
                        for item in v:
                            if item == dish:
                                tem_list.append(ret)
                result = [d for d in result if d in tem_list]
                                     
        for k, v in filter_cond.items():            
            if k == "district":
                tem_list = [] 
                for ret in result:
                    for item in v:
                        if item == ret[k]:
                            tem_list.append(ret)
                result = [d for d in result if d in tem_list]

        for k, v in filter_cond.items():  
            if k == "rating":
                for ret in result:
                    result = [d for d in result if d.get('rating') >= v]
        
        for k, v in filter_cond.items():           
            if k == "name_contains":
                tem_list = [] 
                for ret in result:
                    for item in v:
                        if item in ret["name"]:
                            tem_list.append(ret)
                result = [d for d in result if d in tem_list]
        
        for k, v in filter_cond.items():  
            if k == "price-range":
                tem_list = []
                lower_label, upper_label = float(v.split("-")[0]), float(v.split("-")[1])   
                for ret in result:
                    if ret["price-range"] == "Below $50":
                        temp_price = "$0-50"
                        lower_ret, upper_ret = float(temp_price.split("-")[0][1:]), temp_price.split("-")[1]
                      
                        if lower_ret >= lower_label and upper_ret <= upper_label:
                            tem_list.append(ret) 
                    elif ret["price-range"] == "Above $801":
                        temp_price = "$801-1000"
                        lower_ret, upper_ret = float(temp_price.split("-")[0][1:]), float(temp_price.split("-")[1])     
                        if lower_ret >= lower_label and upper_ret <= upper_label:
                            tem_list.append(ret) 
                    else:
                        lower_ret, upper_ret = float(ret["price-range"].split("-")[0][1:]), float(ret["price-range"].split("-")[1])     
                        if lower_ret >= lower_label and upper_ret <= upper_label:
                            tem_list.append(ret)   
                result = [d for d in result if d in tem_list]
        
        self.query_result = result 
    
    def rank(self, ranking_weight):
        lst_ranked = self.query_result
        ranked_list = []
        score_list = []
        for item in lst_ranked:
            v1 = item["rating"]
            v2 = math.sqrt(((item["address"][0]) - 22.417875)** (2) +((item["address"][1]) - 114.207263)**(2))
            tem_list = []
            if item["price-range"] == "Below $50":
                temp_price = "$0-50"
                lower_ret, upper_ret = float(temp_price.split("-")[0][1:]), float(temp_price.split("-")[1])
                tem_list.append((lower_ret + upper_ret)/2) 
            elif item["price-range"] == "Above $801":
                temp_price = "$801-1000"
                lower_ret, upper_ret = float(temp_price.split("-")[0][1:]), float(temp_price.split("-")[1])     
                tem_list.append((lower_ret + upper_ret)/2) 
            else:
                lower_ret, upper_ret = float(item["price-range"].split("-")[0][1:]), float(item["price-range"].split("-")[1])     
                tem_list.append((lower_ret + upper_ret)/2)   
            v3 = tem_list[0]
            v4 = (float(item["reviews"][2])) / (float(item["reviews"][0]) + float(item["reviews"][1]) + float(item["reviews"][2]))
            ranking_weight_matrix = np.array(ranking_weight)
            v_matrix = np.array((v1,v2,v3,v4))
            score_ret = ranking_weight_matrix.transpose().dot(v_matrix)
            score_list.append([score_ret, item]) 
        score_list.sort(reverse = True)
        for element in  score_list:
            ranked_list.append(element[1])
        self.query_result = ranked_list 
        
    def find_similar(self, restaurant, similiarity_weight, k):
        w1, w2, w3, w4 = similiarity_weight
        lst_ranked = self.query_result
        v_score_list =[] # list of v scores and the corresponding restaurant info
        sim_score_list = [] # list of similarity scores and the corresponding restaurant info
        target_ret_v_score = [] # v scores of the target restaurant 
        result_list =[] # a list contains the top-k similar restaurant 
        for item in lst_ranked:
            v1 = item["rating"]
            v2 = math.sqrt(((item["address"][0]) - 22.417875)** (2) +((item["address"][1]) - 114.207263)**(2))
            tem_list = []
            if item["price-range"] == "Below $50":
                temp_price = "$0-50"
                lower_ret, upper_ret = float(temp_price.split("-")[0][1:]), float(temp_price.split("-")[1])
                tem_list.append((lower_ret + upper_ret)/2) 
            elif item["price-range"] == "Above $801":
                temp_price = "$801-1000"
                lower_ret, upper_ret = float(temp_price.split("-")[0][1:]), float(temp_price.split("-")[1])     
                tem_list.append((lower_ret + upper_ret)/2) 
            else:
                lower_ret, upper_ret = float(item["price-range"].split("-")[0][1:]), float(item["price-range"].split("-")[1])     
                tem_list.append((lower_ret + upper_ret)/2)   
            v3 = tem_list[0]
            v4 = (float(item["reviews"][2])) / (float(item["reviews"][0]) + float(item["reviews"][1]) + float(item["reviews"][2]))
            v_score_list.append([[v1,v2,v3,v4], item]) 
        # score_list.sort(reverse = True)
        for item in v_score_list:
            if restaurant["name"] == item[1]["name"]:
                target_ret_v_score.append(item[0])
        for item in v_score_list:
            score = w1 *(abs(item[0][0]-target_ret_v_score[0][0])) + w2 *(abs(item[0][1]-target_ret_v_score[0][1])) + w3 *(abs(item[0][2]-target_ret_v_score[0][2])) +w4 *(abs(item[0][3]-target_ret_v_score[0][3]))
            sim_score_list.append([score, item[1]])
        sim_score_list.sort()
        
        for item in sim_score_list:
            if item[1]["name"] == restaurant["name"]:
                sim_score_list.remove(item) 
        
        for item in sim_score_list[0:k]:
            result_list.append(item[1])

        for i in range (k, len(sim_score_list)):
            if sim_score_list[i][0] == sim_score_list[i-1][0]:
                result_list.append(sim_score_list[i][1])
            else:
                break
        
        self.query_result = result_list 
    
    def print_query_result(self):
        print('Overall number of query_result: %d' % len(self.query_result))
        for restaurant in self.query_result:
            print json.dumps(restaurant, indent=4)
    
    def return_filtered_data(self):
        return self.query_result

# testClass = Food_Search_Engine('openrice_data.json')
# testClass.load_data('openrice_data.json')
# # #filter_cond = {'name_contains':['Chan Kun', 'Pai Dong'], 'rating': 3.0, 'cuisine':['Guangdong', 'Indian'],'district': ['Sha Tin']}
# filter_cond = {'cuisine': ['Japanese'],'district': ['Sha Tin'], 'price-range': '50-200'}
# testClass.filter(filter_cond)
# testClass.print_query_result()
# testClass.rank([2,0,0,1])
# testClass.print_query_result()
# testClass.reset()
# testClass.find_similar({
#     "cuisine": [
#         "Japanese", 
#         "Food Court"
#     ], 
#     "name": "Pepper Lunch Express", 
#     "district": "Sha Tin", 
#     "rating": 4.5, 
#     "url": "https://s.openrice.com/QrKS0Zrq700", 
#     "reviews": [
#         3, 
#         0, 
#         0
#     ], 
#     "address": [
#         22.4260101, 
#         114.2115065
#     ], 
#     "price-range": "$51-100"
#  },[1,1,1,1],10)
# testClass.print_query_result()