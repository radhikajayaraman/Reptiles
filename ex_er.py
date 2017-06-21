#'http://localhost:2770/compute-media-package?regions=Orissa,Delhi NCR,Pun/Har/Cha/HP/J%26K,Chhattisgarh,TN/Pondicherry,Hyderabad,Uttar Pradesh,Maharashtra/Goa,Bangalore,Rajasthan&date=21-10-16&gender=Female&sub_category=Fuel/Petroleum Products&profile=Value conscious&duration=30&spot_duration=25&budgets=330626&user_id=radhika@amagi.com'
import numpy as np
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

global reg, enabled_value, apii, E_value,ch_l, erm_l,r_l,spot_by_10

with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp

with open("/var/chandni-chowk/configs/app.test.toml") as conffile1:
    config1 = toml.loads(conffile1.read())
reg = config1["app"]["regions"]
# print reg



for i in range(0, 1):
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
    re = requests.get('http://localhost:2770/compute-media-package?regions=Orissa,Delhi NCR,Pun/Har/Cha/HP/J%26K,Chhattisgarh,TN/Pondicherry,Hyderabad,Uttar Pradesh,Maharashtra/Goa,Bangalore,Rajasthan&date=21-10-16&gender=Female&sub_category=Fuel/Petroleum Products&profile=Value conscious&duration=30&spot_duration=25&budgets=330626&user_id=radhika@amagi.com')
    if (re.status_code != 200):
        print re.status_code, ',',
        continue
    else:
        re_t = re.text
        #        print re_t
        data = json.loads(re_t)
        #        print data
#        #### Given gender
#        start = 'gender='
#        end = '&sub_category'
#        gender_in = api[api.find(start) + len(start):api.rfind(end)]
#        print gender_in
#        #### Given spot_duration
#        start = 'spot_duration='
#        end = '&budgets'
#        spot_duration_in = api[api.find(start) + len(start):api.rfind(end)]
#        print spot_duration_in
#        #### Given budget
#        start = 'budgets='
#        end = '&user_id'
#        budget_in = api[api.find(start) + len(start):api.rfind(end)]
#        print budget_in
#        #### profile
#        start = 'profile='
#        end = '&duration'
#        profile_in = api[api.find(start) + len(start):api.rfind(end)]
#        print profile_in
#        #### Response gender
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
                    return Erate[2]
	def er_check():
	    for q in range(0, len(data['package']['region'])):
                if data['package']['region'][q]['channel_order'] == []:
                    continue
                    # If channel_order is not empty, then compute the actual cost
                else:
		    region_name_r = data['package']['region'][q]['region_name']
		    region_cost_r = data['package']['region'][q]['region_cost']
		    discounted_region_cost_r = data['package']['region'][q]['discounted_region_cost']
		    channel_list = []
		    channel_list = data['package']['region'][q]['channel_order']
#		    print channel_list
                    for r in range(0, len(data['package']['region'][q]['channels'])):
			type_r = data['package']['region'][q]['channels'][r]['type']
			secondages_r = data['package']['region'][q]['channels'][r]['secondages']
			channel_name_r = data['package']['region'][q]['channels'][r]['channel_name']
			effective_rate_r = data['package']['region'][q]['channels'][r]['effective_rate']
			cost_r = data['package']['region'][q]['channels'][r]['cost']
			rotates_r = data['package']['region'][q]['channels'][r]['rotates']
			actual_cost_r = data['package']['region'][q]['channels'][r]['actual_cost']
			if region_name_r == 'National' and type_r == 'Spliced':
			    Er_mongo = effective_rate_m("DTH", channel_name_r)
			    calc_cost = float(Er_mongo)*int(rotates_r)*int(spot_duration_out)/10
			    calc_actual_cost = calc_cost/1.1
			    print 'Natio-Spli',',','er_r',',',effective_rate_r,',','rotates',',',rotates_r,',','spot_duration_out',',',spot_duration_out,',','er_m',',',Er_mongo,',','cost_r',',',cost_r,',','actual_cost_r',',',actual_cost_r,',','calc_cost',',',calc_cost,',','calc_actual_cost',',',calc_actual_cost
			elif (region_name_r == 'National' and type_r == 'National'):
			    Er_mongo = effective_rate_m(region_name_r,channel_name_r)	
                	    calc_actual_cost = float(Er_mongo)*int(rotates_r)*int(spot_duration_out)/10
			    print 'NN',',','er_r',',',effective_rate_r,',','rotates',',',rotates_r,',','spot_duration_out',',',spot_duration_out,',','er_m',',',Er_mongo,',','cost_r',',',cost_r,',','actual_cost_r',',',actual_cost_r,',','calc_actual_cost',',',calc_actual_cost
			elif (region_name_r != 'National' and type_r == 'Regional'):
			    Er_mongo = effective_rate_m(region_name_r,channel_name_r)
			    calc_actual_cost = float(Er_mongo)*int(rotates_r)*int(spot_duration_out)/10
			    print '!Natio&Reg',',','region_name_r',',',region_name_r,',','channel_name_r',',',channel_name_r,',','er_r',',',effective_rate_r,',','rotates',',',rotates_r,',','spot_duration_out',',',spot_duration_out,',','er_m',',',Er_mongo,',','cost_r',',',cost_r,',','actual_cost_r',',',actual_cost_r,',','calc_actual_cost',',',calc_actual_cost	
			elif (region_name_r != 'National' and type_r == 'Spliced'):
			    channel_name_r = data['package']['region'][q]['channels'][r]['channel_name']
			    region_name_r = data['package']['region'][q]['region_name']
			    Er_mongo = effective_rate_m(region_name_r,channel_name_r)
			    rotates_r = data['package']['region'][q]['channels'][r]['rotates']
			    spot_by_10 = int(spot_duration_out)/10
			    t_l = []
			    t_l.append(region_name_r)
			    t_l.append(channel_name_r)
			    t_l.append(Er_mongo)
			    t_l.append(rotates_r)
			    print 't_l',t_l
			    		
	er = er_check()
