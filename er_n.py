import numpy from np
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

global reg, enabled_value, apii, E_value

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
    print api
    re = requests.get(api)
    if (re.status_code != 200):
        print re.status_code, ',',
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
        print gender_in
        #### Given spot_duration
        start = 'spot_duration='
        end = '&budgets'
        spot_duration_in = api[api.find(start) + len(start):api.rfind(end)]
        print spot_duration_in
        #### Given budget
        start = 'budgets='
        end = '&user_id'
        budget_in = api[api.find(start) + len(start):api.rfind(end)]
        print budget_in
        #### profile
        start = 'profile='
        end = '&duration'
        profile_in = api[api.find(start) + len(start):api.rfind(end)]
        print profile_in
        #### Response gender
        gender_out = data['package']['gender']
        print gender_out
        #### Response spot_duration
        spot_duration_out = data['package']['spot_duration']
        print spot_duration_out
        #### Response discounted_package_cost
        budget_out = data['package']['discounted_package_cost']
        print budget_out
        #### Response tax
        tax_out = data['package']['tax_amount']
        print tax_out
##############################################################################################
	def effective_rate_m(region_name, channel_name):
            ##effective rate from mongo
            mongo_entire = db.effective_rates.find({})
            for rates in mongo_entire:
                Erate = (rates['region'] + ',', rates['channel'] + ',', rates['effective_rate'])
                region_m = Erate[0][:-1]
                channel_m = Erate[1][:-1]
                if region_name == region_m and channel_name == channel_m:
                    return Erate[2
	def er_check():
	    for q in range(0, len(data['package']['region'])):
                if data['package']['region'][q]['channel_order'] == []:
                    continue
                    # If channel_order is not empty, then compute the actual cost
                else:
                    #sum_c = 0
                    for r in range(0, len(data['package']['region'][q]['channels'])):
			channel_name = data['package']['region'][q]['channels'][r]['channel_name']
                        region_name = data['package']['region'][q]['region_name']
			Er_r = data['package']['region'][q]['channels'][r]['effective_rate']
			type_r = data['package']['region'][q]['channels'][r]['type']
			if region_name == 'National':
			    Er_m = effective_rate_m("DTH", channel_name) 
			else:	
			    Er_m = effective_rate_m(region_name, channel_name)
			##### ER field from response check #####
			#### Regional er is the quote price
			if type_r == 'Regional' and Er_r == Er_m * 1.1 or Er_r == round(Er_m * 1.1):
			    print 'Er_field_check-Pass'
			#### Spliced er is the exact er from mongo ####
			elif type_r == 'Spliced' and Er_r == Er_m:
			    print 'Er_field_check-Pass'
			else:
			    print 'Er_field_check-Fail'
			##### real er check whether it lies between Er_m and Er_r for regional ####
			actual_cost_r = data['package']['region'][q]['channels'][r]['actual_cost']
			secondages_r = data['package']['region'][q]['channels'][r]['secondages']
			real_er_used = actual_cost_r / (secondages_r / spot_duration_out)
			print actual_cost_r,secondages_r,spot_duration_out,real_er_used
			if real_er_used >= Er_m and real_er_used <= (Er_m * 1.1):
			    print 'Real_Er_range-Pass'
			else:
			    print 'Real_Er_range-Fail'
			
			
				
			
