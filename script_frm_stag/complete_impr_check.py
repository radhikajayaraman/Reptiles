from __future__ import division
from pymongo import MongoClient
import toml
import logging
import random
import os
import time
import commands
import json
import re
import pdb
global data, sum_c, total_impr, sum_impr,g, impr
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp
##inputs for the command
genders = ['Male', 'Female', 'Male,Female']
regions = list(db.regions.distinct("region"))
spot_duration = [10,15,20,25,30]
#path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/"
##Number of iterations
for i in range(0,1000):
    cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
    gen = '\"' + random.choice(genders) + '\"'
    reg_iter = random.sample(range(0, len(regions) - 1), random.randint(1, len(regions) - 1))
    current_regions = []
    for j in reg_iter:
        current_regions.append(regions[j])
    	current_regions_str = '\"' + ','.join(current_regions) + '\"'
    	command_str = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " + gen + \
                  " -r " + current_regions_str + cat_prof + " -p " + str(random.randint(5, 99)) + " -s " + str(
        spot_duration[random.randint(0, 4)]) + " -b " + str(random.randint(300000, 1000000))
    	input_command = command_str.replace(',', ' ')
    	output = commands.getoutput(command_str)
        try:
            data = json.loads(output)
        except ValueError:
            continue
    def tvt_mongo_new(r, c, a, g):
	em = db.channel_tvt.find({"channel":c,"region":r,"gender":g,"age":a})
	for document in em:
	    result = document.get("tvt")
	    return result

    def val_reach_spli_mongo(region_name):
	vl = db.reach_split.find({"region":region_name})
	for doc in vl:
            if region_name == "National":
		return doc.get("dth_percent")
	    elif region_name != "National":
		return doc.get("cable_percent")

    def complt_impr():
	for i in range(0,len(data['package']['region'])):
            if data['package']['region'][i]['channel_order'] == []:
                continue
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
		    type_out = data['package']['region'][i]['channels'][j]['type']
		    rotates_out = data['package']['region'][i]['channels'][j]['rotates']
		    if region_name != "National" and type_out == "Spliced":
			tvt_from_mongo = tvt_mongo_new(region_name,channel_name,age,g)
			tvt_specific = tvt_from_mongo * 1000 * rotates
