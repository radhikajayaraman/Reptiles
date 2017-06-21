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

for i in range(0, 500):
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
    elif reg == "One_by_One":
        regions = ["National", "DTH", "Delhi NCR", "Hyderabad", "Bangalore", "TN/Pondicherry", "Kerala",
                   "Pun/Har/Cha/HP/J%26K", "Uttar Pradesh", "West Bengal", "North East", "Orissa", "Jharkhand", "Bihar",
                   "Maharashtra/Goa", "Chhattisgarh", "Rajasthan", "Madhya Pradesh"]
        reg = regions[random.randrange(len(regions))]
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
    re = requests.get(api)
    if (re.status_code != 200):
#        print re.status_code, ',',
        continue
    else:
        re_t = re.text
        data = json.loads(re_t)
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
    def profile_to_tg_mongo(audience_type):
	pf = db.profile_to_tg.find({"audience_type":audience_type})
	for document in pf:
	    result = document.get("tg")
	    r = result.split('/')
	    r_1 = r[0]
	    nccs = list(r_1)
	    return nccs
#	    print result
#	    print r
#	    print r[0]
    def channel_reach(r, c, a, g, nccs):
	em = db.channel_reach.find({"channel":c,"region":r,"gender":g,"age":a,"nccs":nccs})
	for document in em:
	    result = document.get("channel_reach")
	    print result
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
    def channel_mappings_mongo(region_name,type_out,channel_name):
	cov = db.channel_mappings.find({"region":region_name,"type":type_out,"channel_name":channel_name})
	for doc in cov:
	    result = doc.get("coverage")
#	    print result
	    return result
    def chan_reach():
	for i in range(0,len(data['package']['region'])):
            if data['package']['region'][i]['channel_order'] == []:
                continue
                #If channel_order is not empty, then compute the actual cost
            else:
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
		    if gender == 'Male,Female':
			gender_for_tg = ' MF'
		    elif gender == 'Male':
			gender_for_tg = ' M'
		    elif gender == 'Female':
			gender_for_tg = ' F'
		    type_out = data['package']['region'][i]['channels'][j]['type']
		    audience_type =  profile_in + gender_for_tg
		    nccs = profile_to_tg_mongo(audience_type)
		    channel_reach_r = data['package']['region'][i]['channels'][j]['channel_reach']
		    channel_reach_mongo = channel_reach(region_name,channel_name,age,g,nccs)
		    chan_reach =  channel_reach_mongo * 1000 
		    if (region_name != 'National' and type_out == 'Spliced'):
			coverage = channel_mappings_mongo(region_name,type_out,channel_name)
#			print 'coverage',coverage,str(coverage)
			if str(coverage) == 'Cable':
			    value = val_reach_spli_mongo(region_name)
#			    print 'value',value
			elif str(coverage) == 'DTH':
			    value = val_reach_spli_mongo_dth(region_name)
#			    print 'Value',value
			elif str(coverage) == 'Cable+DTH':
			    value = 100
#			    print 'Value',value

			reac = chan_reach * (value / 100)
			print '!N and Spliced:region_name,channel_name,channel_reach_mongo,value,chan_reach*1000,channel_reach_r,calculated_reach',region_name,channel_name,channel_reach_mongo,value,chan_reach,channel_reach_r,reac
			if abs(round(reac)-round(channel_reach_r)) == 1 or abs(round(reac)-round(channel_reach_r)) == 0:
			    res = 'Match'
			    print res
			else:
			    res = 'Mismatch'
			    print res
		    elif (region_name != 'National' and type_out == 'Regional'):
			coverage = channel_mappings_mongo(region_name,type_out,channel_name)
                        if str(coverage) == 'Cable':
                            value = val_reach_spli_mongo(region_name)
                        elif str(coverage) == 'DTH':
                            value = val_reach_spli_mongo_dth(region_name)
                        elif str(coverage) == 'Cable+DTH':
                            value = 100

			reac = chan_reach * (value / 100)
			print '!N and Regional:region_name,channel_name,channel_reach_mongo,value,chan_reach*1000,channel_reach_r,calculated_reach',region_name,channel_name,channel_reach_mongo,value,chan_reach,channel_reach_r,reac
			if abs(round(reac)-round(channel_reach_r)) == 1 or abs(round(reac)-round(channel_reach_r)) == 0:
                            res = 'Match'
			    print res
                        else:
                            res = 'Mismatch'
			    print res
		    elif (region_name == 'National'):
			reac_2 = 0
			reac_2_n = 0
			# National and Spliced -- then -- DTH
			if type_out == 'Spliced':
			    for key,value in data['package']['region'][i]['detailed_region_impressions'].items():
                                region = key
                                channel_reach_mongo = channel_reach(region,channel_name,age,g,nccs)
                                chan_reach =  channel_reach_mongo * 1000 
				coverage = channel_mappings_mongo('DTH',type_out,channel_name)
                        	if str(coverage) == 'Cable':
                            	    value = val_reach_spli_mongo(region)
                        	elif str(coverage) == 'DTH':
                            	    value = val_reach_spli_mongo_dth(region)
                        	elif str(coverage) == 'Cable+DTH':
                            	    value = 100

                                reac_1 = chan_reach * (value/100)
			        reac_2 += reac_1	
			        reac_2_r = data['package']['region'][i]['channels'][j]['channel_reach'] 	
			    if abs(round(reac_2)-round(reac_2_r)) == 1 or abs(round(reac_2)-round(reac_2_r)) == 0:
				res =  'Match'
				print res
			    else:
				res = 'Mismatch'
				print res
				print 'N and Spliced:region_name,channel_name,channel_reach_mongo,value,chan_reach*1000,channel_reach_r,calculated_reach',region_name,channel_name,channel_reach_mongo,value,chan_reach,reac_2_r,reac_2
			elif type_out == 'National':
                            for key,value in data['package']['region'][i]['detailed_region_impressions'].items():
                                region = key
                                channel_reach_mongo = channel_reach(region,channel_name,age,g,nccs)
                                chan_reach =  channel_reach_mongo * 1000
				coverage = channel_mappings_mongo('National',type_out,channel_name)
                                if str(coverage) == 'Cable':
                                    value = val_reach_spli_mongo(region)
                                elif str(coverage) == 'DTH':
                                    value = val_reach_spli_mongo_dth(region)
                                elif str(coverage) == 'Cable+DTH':
                                    value = 100

                                reac_1_n = chan_reach * (value/100)
				reac_2_n += reac_1_n
				reac_2_nr = data['package']['region'][i]['channels'][j]['channel_reach']
				print 'N and N:region_name,channel_name,channel_reach_mongo,value,chan_reach*1000,channel_reach_r,calculated_reach',region_name,channel_name,channel_reach_mongo,value,chan_reach,reac_2_nr,reac_2_n
			    if abs(round(reac_2_n)-round(reac_2_nr)) == 1 or abs(round(reac_2_n)-round(reac_2_nr)) == 0:
                                res = 'Match'
				print res
                            else:
                                res = 'Mismatch'	
				print res
		    r = []
		    r.append(res)
		    print r
	if all(r[0] == item for item in r):
            if r[0] == 'Match':
	        print 'Reach_Match',',',
	    else:
		print 'Reach_Mismatch',',',	   
        else:
	    print 'Reach_Partial_Pass',',',
    rea = chan_reach()
    print api
