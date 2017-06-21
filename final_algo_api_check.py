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
global reg,api
	
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp

with open("/var/chandni-chowk/configs/app.test.toml") as conffile1:
    config1 = toml.loads(conffile1.read())
reg = config1["app"]["regions"]
#print reg



for i in range(0,100):
    def mul_random_regs():
        regions = ['Delhi NCR','Hyderabad','Bangalore','TN/Pondicherry','Kerala','Pun/Har/Cha/HP/J%26K','Uttar Pradesh','West Bengal','North East','Orissa','Jharkhand','Bihar','Maharashtra/Goa','Chhattisgarh','Rajasthan','Madhya Pradesh']
        reg_iter = random.sample(range(0, len(regions) - 1), random.randint(1, len(regions) - 1))
        current_regions = []
        for j in reg_iter:
            current_regions.append(regions[j])
            mul_ran_regs =  ','.join(current_regions)
        return mul_ran_regs
    if reg == "All_regions":
        reg = 'Delhi NCR,Hyderabad,Bangalore,Pun/Har/Cha/HP/J%26K,Maharashtra/Goa,West Bengal,North East,Orissa,Chhattisgarh,Rajasthan,Madhya Pradesh,Jharkhand,Gujarat,Bihar,Uttar Pradesh,TN/Pondicherry,Kerala'
#       print reg
    elif reg == "One_by_One":
        regions = ["National","DTH","Delhi NCR","Hyderabad","Bangalore","TN/Pondicherry","Kerala","Pun/Har/Cha/HP/J%26K","Uttar Pradesh","West Bengal","North East","Orissa","Jharkhand","Bihar","Maharashtra/Goa","Chhattisgarh","Rajasthan","Madhya Pradesh"]
        reg = regions[random.randrange(len(regions))]
#    print reg
    elif reg == "multiple_reg":
        reg = mul_random_regs()
###Inputs needed
    gen_a = ["Male,Female","Male","Female"]
    gen = gen_a[random.randrange(len(gen_a))]
    bud = randint(15000,500000)
    dur = randint(5,99)
    spot_d = ["10","15","20","25","30"]
    spot_dur = spot_d[random.randrange(len(spot_d))]
    cat_prof_a = random.choice(list(open('cat_prof_map_CMPTEST.txt'))).rstrip()
    url ="http://localhost:2770/compute-media-package"
    api = str(url)+'?regions='+mul_random_regs()+'&date=21-10-16&gender='+gen+'&sub_category='+cat_prof_a+'&duration='+str(dur)+'&spot_duration='+str(spot_dur)+'&budgets='+str(bud)+'&user_id=radhika@amagi.com'
#    print api
    re=requests.get(api)
    if (re.status_code != 200):
	print re.status_code,',',api
	continue
    else:
        re_t = re.text
#        print re_t
	data = json.loads(re_t)
#        print data 
#### Given gender
        start = 'gender='
        end = '&sub_category'     
        gender_in = api[api.find(start)+len(start):api.rfind(end)]
#        print gender_in
#### Given spot_duration
	start = 'spot_duration='
    	end = '&budgets'
    	spot_duration_in = api[api.find(start)+len(start):api.rfind(end)]
#    	print spot_duration_in
#### Given budget
    	start = 'budgets='
    	end = '&user_id'
    	budget_in = api[api.find(start)+len(start):api.rfind(end)] 
#    	print budget_in
#### profile
    	start = 'profile='
    	end = '&duration'
    	profile_in = api[api.find(start)+len(start):api.rfind(end)]
#    	print profile_in
#### Response gender
    	gender_out = data['package']['gender']
#    	print gender_out
#### Response spot_duration
    	spot_duration_out = data['package']['spot_duration']
#    	print spot_duration_out
#### Response discounted_package_cost
    	budget_out = data['package']['discounted_package_cost']
#    	print budget_out
#### Response tax
    	tax_out = data['package']['tax_amount']
#   	print tax_out
####Basic check checks the gender,spot_duration, 15% tax amount
    	def basic_check():
	    percent = round(15*(budget_out)/100)
            if ((str(gender_in) == str(gender_out)) or ((str(gender_in) != str(gender_out)) and (str(profile_in) == 'Kids' or str(profile_in) == 'All Adults'))) and (str(spot_duration_in) == str(spot_duration_out)) and (tax_out == percent or tax_out == (percent +1) or tax_out == (percent -1)):
	        print "Gen_SpotD_Tax_Pass",',',
	    else:
	        print "Gen_SpotD_Tax_Fail",',',
	def budget_shoot():
	    bud_diff = int(budget_out) - int(budget_in)
#	    print abs(bud_diff)
	    #### Checking bud_diff is wat percent of input budget
	    bud_diff_percent = round(((abs(bud_diff)*100)/int(budget_in)),2)
	    if bud_diff >= 0:
		if bud_diff_percent > 5:
		    print 'Overshoot',',','bud_diff_percent : '+str(bud_diff_percent),',',budget_in,',',budget_out,',',
		else:
		    print 'No_Overshoot',',','bud_diff_percent : '+str(bud_diff_percent),',',budget_in,',',budget_out,',',
	    elif bud_diff < 0:
		if bud_diff_percent > 5:
		    print 'Under_Utilisation',',','bud_diff_percent : '+str(bud_diff_percent),',',budget_in,',',budget_out,',',
                else:
                    print 'No_Under_Utilisation',',','bud_diff_percent : '+str(bud_diff_percent),',',budget_in,',',budget_out,',',
	def enabled_value_from_mongo(region_name, channel_name):
            mongo_entire = db.channel_mappings.find({})
            for ena in mongo_entire:
                Enab = (ena['region'] + ',', ena['channel_name'] + ',', ena['enabled'])
                region_m = Enab[0][:-1]
                channel_m = Enab[1][:-1]
                if region_name == region_m and channel_name == channel_m:
                    return Enab[2]


        def valid_channel_check():
            #### The channels with enabled value as 2 or 0 should not be selected by the algo
            for k in range(0, len(data['package']['region'])):
                if data['package']['region'][k]['channel_order'] == []:
                    continue
                else:
                    for l in range(0, len(data['package']['region'][k]['channels'])):
                        channel_name = data['package']['region'][k]['channels'][l]['channel_name']
                        region_name = data['package']['region'][k]['region_name']
                        enabled_value = enabled_value_from_mongo(region_name, channel_name)
                        if enabled_value == None and region_name == "National":
                            enabled_value = enabled_value_from_mongo("DTH", channel_name)
                        if enabled_value == 1:
			    res = 'Pass'
                            l = []
                            l.append(res)
                        else:
                            print 'Valid_channels_Fail',',',
            if all(l[0] == item for item in l):
                print 'Valid_channels_Pass',',',
            else:
                print 'Valid_channels_Fail',',',
	def apportioning_er():
            #    actual_cost_compare_discounted_package_cost():
            total_actual_cost = 0
            for m in range(0, len(data['package']['region'])):
                if data['package']['region'][m]['channel_order'] == []:
                    continue
                    # If channel_order is not empty, then compute the actual cost
                else:
                    sum_i = 0
                    for n in range(0, len(data['package']['region'][m]['channels'])):
                        actual_cost_out = data['package']['region'][m]['channels'][n]['actual_cost']
                        sum_i += actual_cost_out
                total_actual_cost += sum_i
            discounted_package_cost_out = data['package']['discounted_package_cost']
            if discounted_package_cost_out == total_actual_cost or discounted_package_cost_out <= (
                total_actual_cost - 1) or discounted_package_cost_out >= (total_actual_cost + 1):
                print 'Apportioning_Er-Pass',',', total_actual_cost,',', discounted_package_cost_out,',',
            else:
                print 'Apportioning_Er-Pass',',', total_actual_cost,',', discounted_package_cost_out,',',
	
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
#	        print result
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
#		        print audience_type
		        nccs = profile_to_tg_mongo(audience_type)
		        tvt_from_mongo = tvt_mongo_new(region_name,channel_name,age,g,nccs)
		        #print tvt_from_mongo
		        tvt =  float(tvt_from_mongo) * 1000 * int(rotates_out)
		        sum_impr = 0
		        if (region_name != 'National' and type_out == 'Spliced'):
			    coverage = channel_mappings_mongo(region_name,type_out,channel_name)
#			    print 'coverage',coverage,str(coverage)
			    if str(coverage) == 'Cable':
			        value = val_reach_spli_mongo(region_name)
#			        print 'value',value
			    elif str(coverage) == 'DTH':
			        value = val_reach_spli_mongo_dth(region_name)
#			        print 'Value',value
			    elif str(coverage) == 'Cable+DTH':
			        value = 100
#			        print 'Value',value

			    impr = tvt * (value / 100)
			    #print 'Calc_Impr_reg_spli',impr,'Resp_Impr_reg_spli',impressions_r,'coverage',coverage,'tvt*1000*rotates',tvt,'Value',value
			    #print 'round',round(impr),round(impressions_r)
			    if abs(round(impr)-round(impressions_r)) == 1 or abs(round(impr)-round(impressions_r)) == 0:
			        res = 'Match'
			        #print res
			    else:
			        res = 'Mismatch'
			        #print res
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
#                                   print 'impr_1',impr_1
			            impr_2 += impr_1	
#			            print 'impr_2',impr_2
			            impr_2_r = data['package']['region'][i]['channels'][j]['impression'] 	
#				    print 'impr_2_r',impr_2_r
				    #print 'National-Spliced','calc_imp',impr_2,'response_imp',impr_2_r,'coverage',coverage,'tvt*1000*rot',tvt,'value',value
			        if abs(round(impr_2)-round(impr_2_r)) == 1 or abs(round(impr_2)-round(impr_2_r)) == 0:
				    res =  'Match'
				    #print res
			        else:
				    res = 'Mismatch'
				    #print res
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
#				    print 'impr_1_n',impr_1_n
				    impr_2_n += impr_1_n
#				    print 'impr_2_n',impr_2_n
				    impr_2_nr = data['package']['region'][i]['channels'][j]['impression']
#                                   print 'impr_2_nr',impr_2_nr
				    #print 'National-National','calc_imp',impr_2_n,'response_imp',impr_2_nr,'coverage',coverage,'tvt*1000*rot',tvt,'value',value
			        if abs(round(impr_2_n)-round(impr_2_nr)) == 1 or abs(round(impr_2_n)-round(impr_2_nr)) == 0:
                                    res = 'Match'
				    #print res
                                else:
                                    res = 'Mismatch'	
				    #print res
		        l = []
		        l.append(res)
		        #print l
	    if all(l[0] == item for item in l):
                if l[0] == 'Match':
	            print 'Impre_Match',',',
	        else:
		    print 'Impre_Mismatch',',',	   
            else:
	        print 'Impre_Partial_Pass',',',
	
	def cutoff_from_mongo(region_name, channel_name):
            # cutoff_rate from mongo
            mongo_entire = db.effective_rates.find({})
            for rates in mongo_entire:
                # print rates
                Erate = (rates['region'] + ',', rates['channel'] + ',', rates['cutoff_rate'])
                region_m = Erate[0][:-1]
                channel_m = Erate[1][:-1]
                if region_name == region_m and channel_name == channel_m:
                    return Erate[2]
	def cutoff_rate_check():
            final_cost_compute = 0
            # cutoff_rate from mongo
            for o in range(0, len(data['package']['region'])):
                if data['package']['region'][o]['channel_order'] == []:
                    continue
                    # If channel_order is not empty, then compute the actual cost
                else:
                    sum_c = 0
                    for p in range(0, len(data['package']['region'][o]['channels'])):
                        channel_name = data['package']['region'][o]['channels'][p]['channel_name']
                        type_out = data['package']['region'][o]['channels'][p]['type']
                        region_name = data['package']['region'][o]['region_name']
                        if region_name == 'National' and (type_out == 'National' or type_out == 'Regional'):
                            region_name = data['package']['region'][o]['region_name']
                        elif region_name == 'National' and type_out == 'Spliced':
                            region_name = 'DTH'
                        else:
                            region_name = data['package']['region'][o]['region_name']
                        E_value = cutoff_from_mongo(region_name, channel_name)
                        print E_value
                        print spot_duration_out
                        actual_compute = E_value * spot_duration_out / 10
                        rotates_out = data['package']['region'][o]['channels'][p]['rotates']
                        cost_compute = actual_compute * rotates_out
                        print 'region_name', region_name, 'channel_name', channel_name, 'type', type_out, 'E_value', E_value, 'actual_compute', actual_compute, 'rotates', rotates_out, 'cost_compute', cost_compute
                        sum_c += cost_compute
                        # print 'sum_c', sum_c
                final_cost_compute += sum_c
                # print 'final', final_cost_compute
            # print 'minimum_package_cost', data['package']['minimum_discounted_cost']
            min_pakg_cost = data['package']['minimum_discounted_cost']
            final = round(final_cost_compute)
            print 'Min_package_cost', ',', min_pakg_cost, ',', 'Final_computed', ',', final, ',',
            if final == min_pakg_cost or min_pakg_cost == (final - 1) or min_pakg_cost == (final + 1):
                print 'Cutoff-Pass',',',
            else:
                print 'Cutoff-Fail',',',
#        basic = basic_check()
#	budg = budget_shoot()
#	valid_chan = valid_channel_check()
#	apportioning_er = apportioning_er() 
#	impr = impre() 
##	cut_off = cutoff_rate_check()
#        print api.replace(',', ' ')
