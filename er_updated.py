from collections import defaultdict
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

global reg, enabled_value, apii, E_value,ch_l, erm_l,r_l,spot_by_10,d

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
		    t_l2 = []
		    t_l = []
		    aal = {}
                    for r in range(0, len(data['package']['region'][q]['channels'])):
			type_r = data['package']['region'][q]['channels'][r]['type']
			secondages_r = data['package']['region'][q]['channels'][r]['secondages']
			channel_name_r = data['package']['region'][q]['channels'][r]['channel_name']
			effective_rate_r = data['package']['region'][q]['channels'][r]['effective_rate']
			cost_r = data['package']['region'][q]['channels'][r]['cost']
			rotates_r = data['package']['region'][q]['channels'][r]['rotates']
			actual_cost_r = data['package']['region'][q]['channels'][r]['actual_cost']
			#### ER from mongo ####
#			Er_mongo = effective_rate_m(region_name_r, channel_name_r)
			#### ER check for National and Spliced channel ####
			if region_name_r == 'National' and type_r == 'Spliced':
			    Er_mongo = effective_rate_m("DTH", channel_name_r)
			    calc_cost = float(Er_mongo)*int(rotates_r)*int(spot_duration_out)/10
			    calc_actual_cost = calc_cost/1.1
#			    print 'Natio-Spli',',','er_r',',',effective_rate_r,',','rotates',',',rotates_r,',','spot_duration_out',',',spot_duration_out,',','er_m',',',Er_mongo,',','cost_r',',',cost_r,',','actual_cost_r',',',actual_cost_r,',','calc_cost',',',calc_cost,',','calc_actual_cost',',',calc_actual_cost
			    if round(actual_cost_r) == round(calc_actual_cost):
				res_er = "Pass"
			    else:
				res_er = "Fail"
#			    print res_er
			elif (region_name_r == 'National' and type_r == 'National') or (region_name_r != 'National' and type_r == 'Regional'):
			    Er_mongo = effective_rate_m(region_name_r,channel_name_r)	
                	    calc_actual_cost = float(Er_mongo)*int(rotates_r)*int(spot_duration_out)/10
			    ####Checking the range ####
			    calc_1 = calc_actual_cost * 1.1
			    if actual_cost_r >= calc_actual_cost and actual_cost_r <= calc_1:
				res_er = "Pass"
			    else:
				res_er = "Fail"
#			    print 'NN&!N-Regio',',','er_r',',',effective_rate_r,',','rotates',',',rotates_r,',','spot_duration_out',',',spot_duration_out,',','er_m',',',Er_mongo,',','cost_r',',',cost_r,',','actual_cost_r',',',actual_cost_r,',','calc_actual_cost',',',calc_actual_cost
#			    print res_er
			elif (region_name_r != 'National' and type_r == 'Spliced'):
			    channel_name_r = data['package']['region'][q]['channels'][r]['channel_name']
			    ch_l = []
			    ch_l.append(channel_name_r)
			    Er_mongo = effective_rate_m(region_name_r,channel_name_r)
			    erm_l = []
			    erm_l.append(Er_mongo)
			    rotates_r = data['package']['region'][q]['channels'][r]['rotates']
			    r_l = []
			    r_l.append(rotates_r)
			    spot_by_10 = int(spot_duration_out)/10
			    t_l = []
			    t_l.append(channel_name_r)
			    t_l.append(region_name_r)
			    t_l.append(Er_mongo)
			    t_l.append(rotates_r)
			    t_l.append(spot_by_10)
			    print t_l
			d = defaultdict(list)
			if t_l != []:
	    		    d[t_l[0]].append(t_l)
			    print d	
			    unique_dicts=list(np.unique(d))
			    print unique_dicts 
#			aal = t_l2
			
#			print aal
#			if aal != []:
#			    for i in defaultdict(aal):
#				print aal[i]
#				print aal[j]
					
#			    tot_l += t_l
#			    print tot_l	
#			    if tot_l != []:
#				d = defaultdict(list)
#				for k, v, u, w, x, y in tot_l:
#				    d[k].append(v).append(u).append(w).append(x).append(y)
#				print d.items()
				
			
			
    er = er_check()		
