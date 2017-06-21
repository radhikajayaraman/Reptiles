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
global data, sum_c
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp
##inputs for the command
genders = ['Male', 'Female', 'Male,Female']
#regions = list(db.regions.distinct("region"))
regions = ['Delhi NCR', 'Hyderabad', 'Bangalore', 'Pun/Har/Cha/HP/J&K', u'Maharashtra/Goa','West Bengal','North East','Orissa','Chhattisgarh','Rajasthan','Madhya Pradesh','Jharkhand','Gujarat','Bihar','Uttar Pradesh','TN/Pondicherry','Kerala','National']
#regions = ['North East','Bangalore']
spot_duration = [10,15,20,25,30]
path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/"
##Number of iterations
for i in range(0,100):
    cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
    gen = '\"' + random.choice(genders) + '\"'
    reg_iter = random.sample(range(0, len(regions) - 1), random.randint(1, len(regions) - 1))
    current_regions = []
    for j in reg_iter:
        current_regions.append(regions[j])
    current_regions_str = '\"' + ','.join(current_regions) + '\"'
    command_str = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " + gen + \
                  " -r " + current_regions_str + cat_prof + " -p " + str(random.randint(5, 99)) + " -s " + str(
        spot_duration[random.randint(0, 4)]) + " -b " + str(random.randint(50000, 300000))
    input_command = command_str.replace(',', ' ')
    status, output = commands.getstatusoutput(command_str)
#    print status
    if status == 0:
        print "Pass",',',
    else:
	print "Fail",',',
    print input_command
