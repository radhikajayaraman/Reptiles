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

global reg, api

with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp

with open("/var/chandni-chowk/configs/app.test.toml") as conffile1:
    config1 = toml.loads(conffile1.read())
reg = config1["app"]["regions"]


# print reg

def category_to_profile_mapping_mongo(category_m):
    c = db.category_to_profile_mapping.find({"category": category_m}).count()
#    print c
    if c is 0 :
        c = db.category_to_profile_mapping.find({"category": 'Miscellaneous'})
    else:
        c = db.category_to_profile_mapping.find({"category": category_m})
    for document in c:
        result = document.get("profiles")
        if result is None or result == "":
            c = db.category_to_profile_mapping.find({"category": 'Miscellaneous'})
            for document in c:
                result = document.get("profiles")
        result1 = result.split(',')
        prof_m = result1[random.randrange(len(result1))]
        return prof_m

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
####Inputs needed
    gen_a = ["Male,Female","Male","Female"]
    gen = gen_a[random.randrange(len(gen_a))]
    bud = randint(15000,500000)
    dur = randint(5,99)
    spot_d = ["10","15","20","25","30"]
    spot_dur = spot_d[random.randrange(len(spot_d))]
    url ="http://localhost:2770/compute-media-package"
    amagitext_to_adex_subcategory = db.amagitext_to_adex_category.find({})
    for z in amagitext_to_adex_subcategory:
#-        amagi_text = (z['amagi_text'])
#-        if "-" in amagi_text:
#-            amagi_t =  amagi_text.split(' - ')
#-            category_m = amagi_t[0]
#-	    category_m = category_used = (z['adex_super_category'])	    
#-            prof_m = category_to_profile_mapping_mongo(category_m)
#-            sub_category_m = amagi_t[1]
#-	else:
#-	    continue
	category_m = (z['adex_super_category'])
	sub_category_m = (z['adex_sub_category'])
	prof_m = category_to_profile_mapping_mongo(category_m)
        if "&" in category_m:
            category_m = category_m.replace("&","%26")
	elif "/" in category_m:
	    category_m = category_m.replace("/","%2F")
	if "&" in sub_category_m:
	    sub_category_m = sub_category_m.replace("&","%26")
	elif "/" in sub_category_m:
	    sub_category_m = sub_category_m.replace("/","%2F")
	
        
#        print category_m, sub_category_m,prof_m
        api = str(url)+'?regions='+mul_random_regs()+'&date=21-10-16&gender='+gen+'&category='+category_m+'&sub_category='+sub_category_m+'&profile='+prof_m+'&duration='+str(dur)+'&spot_duration='+str(spot_dur)+'&budgets='+str(bud)+'&user_id=radhika@amagi.com'
	start_time = time.time()
        re=requests.get(api)
	end_time = time.time()
        if (re.status_code == 200):
            print re.status_code,',',"Pass",',',api
            continue
        else:
	    print re.status_code,',',"Fail",',',api
#            re_t = re.text
#            data = json.loads(re_t)
