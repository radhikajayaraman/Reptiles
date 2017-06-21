import commands
from pymongo import MongoClient
import toml
import logging
import random
from random import randint
import os
import time
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
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp

with open("/var/chandni-chowk/configs/app.test.toml") as conffile1:
    config1 = toml.loads(conffile1.read())
reg = config1["app"]["regions"]
#print reg 

def mul_random_regs():
    regions = ['National','DTH','Delhi NCR','Hyderabad','Bangalore','TN/Pondicherry','Kerala','Pun/Har/Cha/HP/J&K','Uttar Pradesh','West Bengal','North East','Orissa','Jharkhand','Bihar','Maharashtra/Goa','Chhattisgarh','Rajasthan','Madhya Pradesh']
    reg_iter = random.sample(range(0, len(regions) - 1), random.randint(1, len(regions) - 1))
    current_regions = []
    for j in reg_iter:
	current_regions.append(regions[j])
	mul_ran_regs = '\"' + ','.join(current_regions) + '\"'
    return mul_ran_regs

if reg == "All_regions":
    reg = "Delhi NCR,Hyderabad,Bangalore,Pun/Har/Cha/HP/J&K,Maharashtra/Goa,West Bengal,North East,Orissa,Chhattisgarh,Rajasthan,Madhya Pradesh,Jharkhand,Gujarat,Bihar,Uttar Pradesh,TN/Pondicherry,Kerala,National"
    reg = '\"'+reg+'\"'
#    print reg
elif reg == "One_by_One":
    regions = ["National","DTH","Delhi NCR","Hyderabad","Bangalore","TN/Pondicherry","Kerala","Pun/Har/Cha/HP/J&K","Uttar Pradesh","West Bengal","North East","Orissa","Jharkhand","Bihar","Maharashtra/Goa","Chhattisgarh","Rajasthan","Madhya Pradesh"]
    reg = regions[random.randrange(len(regions))]
    reg = '\"'+reg+'\"'
#    print reg
elif reg == "multiple_reg":
    reg = mul_random_regs() 
#    print reg
###Inputs needed
gen_a = ["Male,Female","Male","Female"]
gen = gen_a[random.randrange(len(gen_a))]
gen = '\"'+gen+'\"'
bud = randint(10000,20000)
dur = randint(5,99)
spot_d = ["10","15","20","25","30"]
spot_dur = spot_d[random.randrange(len(spot_d))]
cat_prof = random.choice(list(open('cat_prof_map_api.txt'))).rstrip()
url ="http://stagingapi.amagimix.com/compute-media-package"
###token from API
url1 = "http://stagingapi.amagimix.com/login"
payload1 = '{"email":"radhika@amagi.com","password":"amagi@123"}'
headers1 = {'content-type': 'application/json'}
res = requests.post(url1, data=payload1, headers=headers1)
rep = res.text
d = json.loads(rep)
token = d['data']['user_token']
headers = {'content-type': 'application/json','Authorization':token}
#payload_sample = '{"campaign_id":2135,"age":["22-30"],"gender":["Male","Female"],"region":["Hyderabad","Mumbai"],"budget":"","duration":"7","spot_duration":"10","sub_category":"Agriculture - Farm Equipments","audience_type":["Early Professionals"]}'
for i in range(0,5):
    payload = '{"campaign_id":2135,"age":["22-30"],"gender":['+gen+'],"region":['+reg+'],"budget":"'+str(bud)+'","duration":"'+str(dur)+'","spot_duration":"'+str(spot_dur)+'",'+cat_prof+''
    print payload
    re = requests.post(url, data=payload, headers=headers)
    re_t = re.text
#    print rep
    data = json.loads(re_t)
    
    print data['data']['package']['region'][0]['region_name']
