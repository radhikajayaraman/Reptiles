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
print "Status,Status_code,api_call"	
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp

with open("/var/chandni-chowk/configs/app.test.toml") as conffile1:
    config1 = toml.loads(conffile1.read())
reg = config1["app"]["regions"]
#print reg 

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


def cat_subcat_def():
    a = randint(1,445)
    N = db.amagitext_to_adex_category.find().limit(-1).skip(a).next()
    category_used = (N['adex_super_category'])
    sub_category_used = (N['adex_sub_category'])
#    print "N, category_used, sub_category_used", N, category_used, sub_category_used
    if "&" in category_used:
        category_used = category_used.replace("&","%26")
    elif "/" in category_used:
        category_used = category_used.replace("/","%2F")
    if "&" in sub_category_used:
        sub_category_used = sub_category_used.replace("&","%26")
    elif "/" in sub_category_used:
        sub_category_used = sub_category_used.replace("/","%2F")
    prof_m = category_to_profile_mapping_mongo(category_used)
#    print category_used, sub_category_used, prof_m
    return category_used, sub_category_used, prof_m

def mul_random_regs():
    regions = db.channel_mappings.distinct("region",{"enabled":1})
    regions = [r.replace("&","%26") for r in regions]
    if 'National' in regions: regions.remove('National')
    if 'DTH' in regions: regions.remove('DTH')
    reg_iter = random.sample(range(0, len(regions) - 1), random.randint(1, len(regions) - 1))
    current_regions = []
    for j in reg_iter:
        current_regions.append(regions[j])
#    print current_regions
    if (('AP/Telangana' and 'Hyderabad') or ('Hyderabad' and 'Rest of Andhra Pradesh')) in current_regions:current_regions.remove('Hyderabad')
    if ('AP/Telangana' and 'Rest of Andhra Pradesh') in r: r.remove('Rest of Andhra Pradesh')
    if (('Karnataka' and 'Bangalore') or ('Bangalore' and 'Rest of Karnataka')) in current_regions:current_regions.remove('Bangalore')
    if ('Karnataka' and 'Rest of Karnataka') in current_regions:current_regions.remove('Rest of Karnataka')
    if (('TN/Pondicherry' and 'Chennai') or ('Chennai' and 'Rest of Tamil Nadu')) in current_regions:current_regions.remove('Chennai')
    if ('TN/Pondicherry' and 'Rest of Tamil Nadu') in current_regions:current_regions.remove('Rest of Tamil Nadu')
    if (('Maharashtra/Goa' and 'Mumbai') or ('Mumbai' and 'Rest of Maharashtra')) in current_regions:current_regions.remove('Mumbai')
    if ('Maharashtra/Goa' and 'Rest of Maharashtra') in current_regions:current_regions.remove('Rest of Maharashtra')
    mul_ran_regs =  ','.join(current_regions)
    return mul_ran_regs
for i in range(0,1000):
###Inputs needed
    gen_a = ["Male,Female","Male","Female"]
    gen = gen_a[random.randrange(len(gen_a))]
    bud = randint(1000,500000)
    dur = randint(5,99)
    spot_d = ["10","15","20","25","30"]
    spot_dur = spot_d[random.randrange(len(spot_d))]
    url ="http://localhost:2770/compute-media-package"
    mul_reg = mul_random_regs()
    category_used, sub_category_used, prof_m = cat_subcat_def()
    api = str(url)+'?regions='+mul_reg+'&date=21-10-16&gender='+gen+'&category='+category_used+'&sub_category='+sub_category_used+'&profile='+prof_m+'&duration='+str(dur)+'&spot_duration='+str(spot_dur)+'&budgets='+str(bud)+'&user_id=radhika@amagi.com'
#    api = str(url)+'?regions='+mul_reg+'&date=21-10-16&gender='+gen+'&sub_category='+cat_prof_a+'&duration='+str(dur)+'&spot_duration='+str(spot_dur)+'&budgets='+str(bud)+'&user_id=radhika@amagi.com'
#    print api
    re=requests.get(api)
    re_t = re.status_code
    if str(re_t) == '200':
	print 'Pass',',',
    else:
	print 'Fail',',',
    print re_t,',',
    print api
#    print api.replace(',',' ')
