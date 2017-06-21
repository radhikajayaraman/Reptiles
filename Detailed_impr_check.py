import commands
from pymongo import MongoClient
import toml
import logging
import random
from random import randint
import re
import os
import time
import commands
import json
import pdb
import requests, json
import sys
import urllib
global reg, enabled_value, apii, E_value,impr_1, impr_n

with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp

with open("/var/chandni-chowk/configs/app.test.toml") as conffile1:
    config1 = toml.loads(conffile1.read())
reg = config1["app"]["regions"]
# print reg



for i in range(0, 1000):
    def mul_random_regs():
        regions = ['Delhi NCR', 'Hyderabad', 'Bangalore', 'TN/Pondicherry', 'Kerala', 'Pun/Har/Cha/HP/J%26K',
                   'Uttar Pradesh', 'West Bengal', 'North East', 'Orissa', 'Jharkhand', 'Bihar', 'Maharashtra/Goa',
                   'Chhattisgarh', 'Rajasthan', 'Madhya Pradesh']
        reg_iter = random.sample(range(0, len(regions) - 1), random.randint(1, len(regions) - 1))
        current_regions = []
        for j in reg_iter:
            current_regions.append(regions[j])
            mul_ran_regs = ','.join(current_regions)
        return mul_ran_regs


    if reg == "All_regions":
        reg = 'Delhi NCR,Hyderabad,Bangalore,Pun/Har/Cha/HP/J%26K,Maharashtra/Goa,West Bengal,North East,Orissa,Chhattisgarh,Rajasthan,Madhya Pradesh,Jharkhand,Gujarat,Bihar,Uttar Pradesh,TN/Pondicherry,Kerala'
    # print reg
    elif reg == "One_by_One":
        regions = ["National", "DTH", "Delhi NCR", "Hyderabad", "Bangalore", "TN/Pondicherry", "Kerala",
                   "Pun/Har/Cha/HP/J%26K", "Uttar Pradesh", "West Bengal", "North East", "Orissa", "Jharkhand", "Bihar",
                   "Maharashtra/Goa", "Chhattisgarh", "Rajasthan", "Madhya Pradesh"]
        reg = regions[random.randrange(len(regions))]
    # print reg
    elif reg == "multiple_reg":
        reg = mul_random_regs()
    ###Inputs needed
    gen_a = ["Male,Female", "Male", "Female"]
    gen = gen_a[random.randrange(len(gen_a))]
    bud = randint(0, 500000)
    dur = randint(5, 99)
    spot_d = ["10", "15", "20", "25", "30"]
    spot_dur = spot_d[random.randrange(len(spot_d))]
    cat_prof_a = random.choice(list(open('cat_prof_map_CMPTEST.txt'))).rstrip()
    url = "http://localhost:2770/compute-media-package"
    api = str(
        url) + '?regions=' + mul_random_regs() + '&date=21-10-16&gender=' + gen + '&sub_category=' + cat_prof_a + '&duration=' + str(
        dur) + '&spot_duration=' + str(spot_dur) + '&budgets=' + str(bud) + '&user_id=radhika@amagi.com'
#    print api
#    re = requests.get(api)
#    re = requests.get('http://localhost:2770/compute-media-package?regions=Pun/Har/Cha/HP/J%26K,Uttar Pradesh,Orissa,Rajasthan&date=21-10-16&gender=Female&sub_category=Durables&profile=Young Adults&duration=93&spot_duration=20&budgets=470829&user_id=radhika@amagi.com')	
    re = requests.get('http://localhost:2770/compute-media-package?regions=Maharashtra/Goa,West Bengal,Hyderabad,Chhattisgarh,Bangalore,Delhi NCR,North East,Uttar Pradesh,Pun/Har/Cha/HP/J%26K,Rajasthan,Bihar&date=21-10-16&gender=Female&sub_category=Auto&profile=Young Adults&duration=60&spot_duration=20&budgets=446107&user_id=radhika@amagi.com')
    if (re.status_code != 200):
#        print re.status_code, ',',
        continue
    else:
        re_t = re.text
        #        print re_t
        data = json.loads(re_t)
        #        print data
        #### Given gender
        start = 'gender='
        end = '&sub_category'
        gender_in = api[api.find(start) + len(start):api.rfind(end)]
#        print gender_in
        #### Given spot_duration
        start = 'spot_duration='
        end = '&budgets'
        spot_duration_in = api[api.find(start) + len(start):api.rfind(end)]
#        print spot_duration_in
        #### Given budget
        start = 'budgets='
        end = '&user_id'
        budget_in = api[api.find(start) + len(start):api.rfind(end)]
#        print budget_in
        #### profile
        start = 'profile='
        end = '&duration'
        profile_in = api[api.find(start) + len(start):api.rfind(end)]
#        print profile_in
        #### Response gender
        gender_out = data['package']['gender']
#        print gender_out
        #### Response spot_duration
        spot_duration_out = data['package']['spot_duration']
#        print spot_duration_out
        #### Response discounted_package_cost
        budget_out = data['package']['discounted_package_cost']
#        print budget_out
        #### Response tax
        tax_out = data['package']['tax_amount']
#        print tax_out

    def tvt_mongo_new(r, c, a, g):
	em = db.channel_tvt.find({"channel":c,"region":r,"gender":g,"age":a})
	for document in em:
	    result = document.get("tvt")
	    return result

    def val_reach_spli_mongo(region_name):
	vl = db.reach_split.find({"region":region_name})
	for doc in vl:
	    if region_name != "National":
		return doc.get("cable_percent")
    def val_reach_spli_mongo_dth(region_name):
	vl = db.reach_split.find({"region":region_name})
	for doc in vl:
	    if region_name != "National":
		return doc.get("dth_percent")
    def impre():
	total_impr = 0
	for i in range(0,len(data['package']['region'])):
            if data['package']['region'][i]['channel_order'] == []:
                continue
                #If channel_order is not empty, then compute the actual cost
            else:
		sum_impr = 0
                region_name = data['package']['region'][i]['region_name']
                for j in range(0,len(data['package']['region'][i]['channels'])):
		    channel_name = data['package']['region'][i]['channels'][j]['channel_name']
		    age = data['package']['age']
		    gender = data['package']['gender']
		    if gender == 'Male,Female':
			g = ["Male","Female"]
		    elif gender == 'Male':
			g = ["Male"]
		    elif gender == 'Female':
			g = ["Female"]
		    type_out = data['package']['region'][i]['channels'][j]['type']
		    rotates_out = data['package']['region'][i]['channels'][j]['rotates']
		    impressions_r = data['package']['region'][i]['channels'][j]['impression']
		    tvt_from_mongo = tvt_mongo_new(region_name,channel_name,age,g)
		    tvt =  float(tvt_from_mongo) * 1000 * int(rotates_out)
		    sum_impr = 0
		    if (region_name != 'National' and type_out == 'Spliced'):
			cable_value = val_reach_spli_mongo(region_name)
			impr = tvt * (cable_value / 100)
			print 'Region-Spliced',',','Region',',',region_name,',','Channel',',',channel_name,',','Type',',',type_out,',','Gender',',',gender,',','age',',',age,',','rotates',',',rotates_out,',','tvt_mong',',',tvt_from_mongo,',','tvt*1000*rot',',',tvt,',','Cable',',',cable_value,',','tvt*(cabl/100)',',',impr,',','Resp_Impr_reg_spli',',',impressions_r
#			if round(impr) == round(impressions_r):
#			    print 'Match'
#			else:
#			    print 'Mismatch'
		    elif (region_name != 'National' and type_out == 'Regional'):
			impr = tvt
			print 'Region-Regional',',','Region',',',region_name,',','Channel',',',channel_name,',','Type',',',type_out,',','Gender',',',gender,',','age',',',age,',','rotates',',',rotates_out,',','tvt_mong',',',tvt_from_mongo,',','tvt*1000*rot',',',tvt,',','calc_impr',',',impr,',','Resp_Impr_reg_spli',',',impressions_r
#			print 'Calc_Impr_reg_regio',impr,'Resp_Impr_reg_regio',impressions_r
#			if round(impr) == round(impressions_r):
#                            print 'Match'
#                        else:
#                            print 'Mismatch'
		    elif (region_name == 'National'):
			impr_2 = 0
			impr_2_n = 0
			if type_out == 'Spliced':
			    for key,value in data['package']['region'][i]['detailed_region_impressions'].items():
                                region = key
                                tvt_from_mongo = tvt_mongo_new(region,channel_name,age,g)
                                tvt =  float(tvt_from_mongo) * 1000 * int(rotates_out)
                                dth_value = val_reach_spli_mongo_dth(region)
                                impr_1 = tvt * (dth_value/100)
#                                print 'impr_1',impr_1
			        impr_2 += impr_1	
#			        print 'impr_2',impr_2
			        impr_2_r = data['package']['region'][i]['channels'][j]['impression'] 	
				print 'National-Spliced',',','Region',',',region_name,',','Channel',',',channel_name,',','Type',',',type_out,',','Gender',',',gender,',','age',',',age,',','rotates',',',rotates_out,',','tvt_mong',',',tvt_from_mongo,',','tvt*1000*rot',',',tvt,',','dth_value',',',dth_value,',','tvt*(dth/100)',',',impr_1,',','impr_2_r',',',impr_2_r,',','Resp_Impr_reg_spli',',',impr_2_r
#				print 'impr_2_r',impr_2_r
#			    if round(impr_2) == round(impr_2_r):
#				print 'Match'
#			    else:
#				print 'Mismatch'
			elif type_out == 'National':
                            for key,value in data['package']['region'][i]['detailed_region_impressions'].items():
                                region = key
                                tvt_from_mongo = tvt_mongo_new(region,channel_name,age,g)
                                tvt =  float(tvt_from_mongo) * 1000 * int(rotates_out)
                                impr_1_n = tvt
#				print 'impr_1_n',impr_1_n
				impr_2_n += impr_1_n
#				print 'impr_2_n',impr_2_n
				impr_2_nr = data['package']['region'][i]['channels'][j]['impression']
				print 'National-Spliced',',','Region',',',region_name,',','Channel',',',channel_name,',','Type',',',type_out,',','Gender',',',gender,',','age',',',age,',','rotates',',',rotates_out,',','tvt_mong',',',tvt_from_mongo,',','tvt*1000*rot',',',tvt,',','Calc_impr',',',impr_1_n,',','impr_2_n',',',impr_2_n,',','response',',',impr_2_nr
#                                print 'impr_2_nr',impr_2_nr
#			    if round(impr_2_n) == round(impr_2_nr):
#                                print 'Match'
#                            else:
#                                print 'Mismatch'	
    imp = impre()
    print api
