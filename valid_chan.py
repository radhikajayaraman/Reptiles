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
	print re.status_code,',',
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
			    print 'Valid_channels_Fail'
	    if all(l[0] == item for item in l):
                print 'Valid_channels_Pass'
            else:
                print 'Valid_channels_Fail'	
    v = valid_channel_check()
    print api
