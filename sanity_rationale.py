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
import time
global reg, api
#print "region_name,channel_name,rationale,api"
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp

with open("/var/chandni-chowk/configs/app.test.toml") as conffile1:
    config1 = toml.loads(conffile1.read())
reg = config1["app"]["regions"]


def profile_to_tg_mongo(audience_type):
    pf = db.profile_to_tg.find({"audience_type":audience_type})
    for document in pf:
	result = document.get("tg")
	r = result.split('/')
	r_1 = r[0]
	nccs = list(r_1)
	return nccs
def rationale_mongo(r, c, a, g, nccs):
    em = db.rationale.find({"channel":c,"region":r,"gender":g,"age":a,"nccs":nccs})
    for doc in em :
	status = doc.get("status")
	rationa = doc.get("rationale")
	return status, rationa


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
    if len(current_regions) == 0 : mul_ran_regs = "National"
    return mul_ran_regs

for i in range(0,100):
#### Inputs Needed	
    reg = mul_random_regs()
    gen_a = ["Male,Female","Male","Female"]
    gen = gen_a[random.randrange(len(gen_a))]
    bud = randint(15000,500000)
    dur = randint(5,99)
    spot_d = ["10","15","20","25","30"]
    regions = db.channel_mappings.distinct("region",{"enabled":1})
    regions = [r.replace("&","%26") for r in regions]
    if 'National' in regions: regions.remove('National')
    if 'DTH' in regions: regions.remove('DTH')
    #print regions
    reg_one_by_one = regions[random.randrange(len(regions))]
#    reg_one_by_one = "Pun/Har/Cha/HP/J%26K"
    spot_dur = spot_d[random.randrange(len(spot_d))]
    category_used, sub_category_used, prof_m = cat_subcat_def()
    url ="http://localhost:2770/compute-media-package"
    api = str(url)+'?regions='+reg_one_by_one+'&date=21-10-16&gender='+gen+'&category='+category_used+'&sub_category='+sub_category_used+'&profile='+prof_m+'&duration='+str(dur)+'&spot_duration='+str(spot_dur)+'&budgets='+str(bud)+'&user_id=radhika@amagi.com'
    start_time = time.time()
    re=requests.get(api)
    end_time = time.time()
    if (re.status_code != 200):
	print re.status_code,',',api
	continue
    else:
#	print api
        re_t = re.text
#        print re_t
	data = json.loads(re_t)
	def rationale_check():
    	    for i in range(0,len(data['package']['region'])):
		if data['package']['region'][i]['channel_order'] == []:
	    	    continue
		else:
	    	    for j in range(0,len(data['package']['region'][i]['channels'])):
		    	region_name = data['package']['region'][i]['region_name']
		    	channel_name = data['package']['region'][i]['channels'][j]['channel_name']
		    	rationale = data['package']['region'][i]['channels'][j]['rationale']
			reach = data['package']['region'][i]['channels'][j]['reach']
			cpv = data['package']['region'][i]['channels'][j]['cpv']
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
			start = 'profile='
		        end = '&duration'
		        profile_in = api[api.find(start)+len(start):api.rfind(end)]			
			audience_type =  profile_in + gender_for_tg
			nccs = profile_to_tg_mongo(audience_type)
			print region_name, channel_name
			if region_name == "National":
			    status = "No_data"
			    rationale_from_mongo = "No_data"
			else:
                            status, rationale_from_mongo = rationale_mongo(region_name,channel_name,age,g,nccs)
						
		    	print region_name,',', channel_name ,',',rationale,',',reach,',',cpv,',',status,',',rationale_from_mongo
#			print rationale,',', region_name,',', channel_name ,',', reach,',', cpv
	def san_rationale():
    	    for i in range(0,len(data['package']['region'])):
        	if data['package']['region'][i]['channel_order'] == []:
            	    continue
        	else:
            	    for j in range(0,len(data['package']['region'][i]['channels'])):
			if "rationale" in data['package']['region'][i]['channels'][j]:
		    	    print "------------------------------Pass"
			else:
		    	    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Fail",',',api
	
	r = rationale_check()

#	ra = san_rationale()
	print api
	print "_______________________________________________________________________________"
#print api


