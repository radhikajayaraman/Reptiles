import toml
import logging
import random
from random import randint
import os
import time
from pymongo import MongoClient
import commands
import json
import re
import pdb
import requests, json
import sys
import urllib
global reg,a,b
	
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config['app']['mongo_conn_str'])
db = mongo_client.dsp

with open("/var/chandni-chowk/configs/app.test.toml") as conffile1:
    config1 = toml.loads(conffile1.read())
reg = config1["app"]["regions"]
#print reg 


for i in range(0,1000):
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
#	print reg
    elif reg == "One_by_One":
    	regions = ["National","DTH","Delhi NCR","Hyderabad","Bangalore","TN/Pondicherry","Kerala","Pun/Har/Cha/HP/J%26K","Uttar Pradesh","West Bengal","North East","Orissa","Jharkhand","Bihar","Maharashtra/Goa","Chhattisgarh","Rajasthan","Madhya Pradesh"]
    	reg = regions[random.randrange(len(regions))]
#    print reg
    elif reg == "multiple_reg":
    	reg = mul_random_regs() 
###Inputs needed
    gen_a = ["Male,Female","Male","Female"]
    gen = gen_a[random.randrange(len(gen_a))]
    bud = randint(0,9999000)
    dur = randint(5,99)
    spot_d = ["10","15","20","25","30"]
    spot_dur = spot_d[random.randrange(len(spot_d))]
    cat_prof_a = random.choice(list(open('cat_prof_map_CMPTEST.txt'))).rstrip()
    url ="http://localhost:2770/compute-media-package"
    api = str(url)+'?regions='+mul_random_regs()+'&date=21-10-16&gender='+gen+'&sub_category='+cat_prof_a+'&duration='+str(dur)+'&spot_duration='+str(spot_dur)+'&budgets='+str(bud)+'&user_id=radhika@amagi.com'
#    print api
    re=requests.get(api)
    re_t = re.status_code
    if str(re_t) == '200':
	print 'Pass',',',
    else:
	print 'Fail',',',
    print re_t,',',
    print api
