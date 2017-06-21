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
#    api = 'http://localhost:2770/compute-media-package?regions=TN/Pondicherry,Bihar,Orissa&date=21-10-16&gender=Female&sub_category=Fuel/Petroleum Products&profile=College Adults&duration=22&spot_duration=20&budgets=23776&user_id=radhika@amagi.com'
    #print api
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
    def er_mongo(r,c,t):
	em = db.effective_rates.find({"channel":c,"region":r})
	for document in em:
	    if t == 'Spliced':
		result = document.get("effective_rate")
		return result
	    elif t == 'Regional' or t == 'National':
		result = document.get("effective_rate")
		fin = result * 1.1
		return fin	
    def tvt_mongo_new(r, c, a, g, nccs):
	em = db.channel_tvt.find({"channel":c,"region":r,"gender":g,"age":a,"nccs":nccs})
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
    def channel_mappings_mongo(region_name,type_out,channel_name):
	cov = db.channel_mappings.find({"region":region_name,"type":type_out,"channel_name":channel_name})
	for doc in cov:
	    result = doc.get("coverage")
#	    print result
	    return result
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
		    if gender == 'Male,Female':
			gender_for_tg = ' MF'
		    elif gender == 'Male':
			gender_for_tg = ' M'
		    elif gender == 'Female':
			gender_for_tg = ' F'
		    type_out = data['package']['region'][i]['channels'][j]['type']
		    rotates_out = data['package']['region'][i]['channels'][j]['rotates']
		    impressions_r = data['package']['region'][i]['channels'][j]['impression']
		    audience_type =  profile_in + gender_for_tg
		    cpv_r = data['package']['region'][i]['channels'][j]['cpv']
		    #value = 1
#		    print audience_type
		    nccs = profile_to_tg_mongo(audience_type)
		    tvt_from_mongo = tvt_mongo_new(region_name,channel_name,age,g,nccs)
		    #print tvt_from_mongo
		    tvt =  float(tvt_from_mongo) * 1000 * int(rotates_out)
		    sum_impr = 0
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

			impr = tvt * (value / 100)
			#print 'Calc_Impr_reg_spli',impr,'Resp_Impr_reg_spli',impressions_r,'coverage',coverage,'tvt*1000*rotates',tvt,'Value',value
			#print 'round',round(impr),round(impressions_r)
			if abs(round(impr)-round(impressions_r)) == 1 or abs(round(impr)-round(impressions_r)) == 0:
			    res = 'Match'
			    #print res
			else:
			    res = 'Mismatch'
			    #print res
			er_mon = er_mongo(region_name,channel_name,type_out)
			if impr == 0 and cpv_r == 0:
			    ress = "C_Match"
			else:
			    cpv = (er_mon / impr ) * rotates_out
#			    print 'Er_mongo,impr_calc,rotates',er_mon , impr , rotates_out
#			    print '!National n spli',cpv,'cpv_response',cpv_r
			    if round(abs(round(cpv,2) - round(cpv_r,2))) == 0 or round(abs(round(cpv,2) - round(cpv_r,2))) == 1:
				ress = "C_Match"
			    else:
				ress = "C_Mismatch"	
#			    print cpv,cpv_r
		    elif (region_name != 'National' and type_out == 'Regional'):
			coverage = channel_mappings_mongo(region_name,type_out,channel_name)
                        if str(coverage) == 'Cable':
                            value = val_reach_spli_mongo(region_name)
                        elif str(coverage) == 'DTH':
                            value = val_reach_spli_mongo_dth(region_name)
                        elif str(coverage) == 'Cable+DTH':
                            value = 100

			impr = tvt * (value / 100)
			#print 'Calc_Impr_reg_regio',impr,'Resp_Impr_reg_regio',impressions_r,'coverage',coverage,'tvt*1000*rotates',tvt,'Value',value
			if abs(round(impr)-round(impressions_r)) == 1 or abs(round(impr)-round(impressions_r)) == 0:
                            res = 'Match'
			    #print res
                        else:
                            res = 'Mismatch'
			    #print res
			er_mon = er_mongo(region_name,channel_name,type_out)
			if impr == 0 and cpv_r == 0:
                            ress = "C_Match"
                        else:
                            cpv = (er_mon / impr ) * rotates_out
#			    print 'Er_mongo,impr_calc,rotates',er_mon , impr , rotates_out
#			    print '!National n regional',cpv,'cpv_response',cpv_r
			    if round(abs(round(cpv,2) - round(cpv_r,2))) == 0 or round(abs(round(cpv,2) - round(cpv_r,2))) == 1:
                                ress = "C_Match"
                            else:
                                ress = "C_Mismatch"
#			print cpv,cpv_r
		    elif (region_name == 'National'):
			impr_2 = 0
			impr_2_n = 0
			# National and Spliced -- then -- DTH
			if type_out == 'Spliced':
			    for key,value in data['package']['region'][i]['detailed_region_impressions'].items():
                                region = key
                                tvt_from_mongo = tvt_mongo_new(region,channel_name,age,g,nccs)
                                tvt =  float(tvt_from_mongo) * 1000 * int(rotates_out)
				coverage = channel_mappings_mongo('DTH',type_out,channel_name)
                        	if str(coverage) == 'Cable':
                            	    value = val_reach_spli_mongo(region)
                        	elif str(coverage) == 'DTH':
                            	    value = val_reach_spli_mongo_dth(region)
                        	elif str(coverage) == 'Cable+DTH':
                            	    value = 100

                                impr_1 = tvt * (value/100)
#                                print 'impr_1',impr_1
			        impr_2 += impr_1	
#			        print 'impr_2',impr_2
			        impr_2_r = data['package']['region'][i]['channels'][j]['impression'] 	
#				print 'impr_2_r',impr_2_r
				#print 'National-Spliced','calc_imp',impr_2,'response_imp',impr_2_r,'coverage',coverage,'tvt*1000*rot',tvt,'value',value
			    if abs(round(impr_2)-round(impr_2_r)) == 1 or abs(round(impr_2)-round(impr_2_r)) == 0:
				res =  'Match'
				#print res
			    else:
				res = 'Mismatch'
				#print res
			    er_mon = er_mongo('DTH',channel_name,type_out)
			    if impr_2 == 0 and cpv_r == 0:
                                ress = "C_Match"
                            else:
			        cpv = (er_mon / impr_2 ) * rotates_out
#			        print 'Er_mongo,impr_calc,rotates',er_mon , impr_2 , rotates_out
#			        print 'National n Spliced',cpv,'cpv_response',cpv_r
				if round(abs(round(cpv,2) - round(cpv_r,2))) == 0 or round(abs(round(cpv,2) - round(cpv_r,2))) == 1:
                                    ress = "C_Match"
                                else:
                                    ress = "C_Mismatch"
#			    print cpv,cpv_r
			elif type_out == 'National':
                            for key,value in data['package']['region'][i]['detailed_region_impressions'].items():
                                region = key
                                tvt_from_mongo = tvt_mongo_new(region,channel_name,age,g,nccs)
                                tvt =  float(tvt_from_mongo) * 1000 * int(rotates_out)
				coverage = channel_mappings_mongo('National',type_out,channel_name)
                                if str(coverage) == 'Cable':
                                    value = val_reach_spli_mongo(region)
                                elif str(coverage) == 'DTH':
                                    value = val_reach_spli_mongo_dth(region)
                                elif str(coverage) == 'Cable+DTH':
                                    value = 100

                                impr_1_n = tvt * (value/100)
#				print 'impr_1_n',impr_1_n
				impr_2_n += impr_1_n
#				print 'impr_2_n',impr_2_n
				impr_2_nr = data['package']['region'][i]['channels'][j]['impression']
#                                print 'impr_2_nr',impr_2_nr
				#print 'National-National','calc_imp',impr_2_n,'response_imp',impr_2_nr,'coverage',coverage,'tvt*1000*rot',tvt,'value',value
			    if abs(round(impr_2_n)-round(impr_2_nr)) == 1 or abs(round(impr_2_n)-round(impr_2_nr)) == 0:
                                res = 'Match'
				#print res
                            else:
                                res = 'Mismatch'	
				#print res
			    er_mon = er_mongo('National',channel_name,type_out)
			    if impr_2_n == 0 and cpv_r == 0:
                                ress = "C_Match"
                            else:
                                cpv = (er_mon / impr_2_n ) * rotates_out
#			        print 'Er_mongo,impr_calc,rotates',er_mon , impr_2_n , rotates_out
#                               print 'National n National',cpv,'cpv_response',cpv_r
				if round(abs(round(cpv,2) - round(cpv_r,2))) == 0 or round(abs(round(cpv,2) - round(cpv_r,2))) == 1:
                                    ress = "C_Match"
                                else:
                                    ress = "C_Mismatch"
#			    print cpv,cpv_r
		    l = []
		    l.append(res)
		    c = []
		    c.append(ress)
#		    print c
#		    print l
	if all(c[0] == item for item in c):
	    if c[0] == 'C_Match':
		print 'CPV_Match',',',
	    else:
		print 'CPV_Mismatch',',',
	else:
	    print 'CPV_Partial_Pass'
	if all(l[0] == item for item in l):
            if l[0] == 'Match':
	        print 'Impre_Match',',',
	    else:
		print 'Impre_Mismatch',',',	   
        else:
	    print 'Impre_Partial_Pass',',',
    imp = impre()
    print api
