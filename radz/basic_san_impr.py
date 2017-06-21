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
import csv
import sys
global data, sum_c, total_impr, sum_impr,g, impr
#print "Tax,Gender,Budget_Shoot,Budget_diff_percentage,Result_Cost,Result_Discount,Result_Cutoff,Input_command"
#print "Result_impression, Impression_from_response,Impression_calcltd,Input_command"
print "Result_impression, Impression_from_response, Input_command"
##config file
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
#    print input_command,',',
#    command_str = "python /home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+ -g 'Female' -r 'Bihar, Kerala, Jharkhand, Orissa' -c 'Hair Care' -m 'Early Professionals' -p 7 -s 25 -b 411920"
#    print command_str
#    command_str = "python /home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+ -g 'Male,Female' -r 'Uttar Pradesh,Rajasthan' -c 'Food & Beverages' -m 'Teens' -p 10 -s 10 -b 15000"
    	output = commands.getoutput(command_str)
#    print output
        try:
            data = json.loads(output)
        except ValueError:
            continue

    def basic_san():
	if data['package']['package_impressions'] != 0:
	    print "Pass",',',data['package']['package_impressions'],',',input_command
	else:
	    print "Fail",',',data['package']['package_impressions'],',',input_command
    impr = basic_san()
