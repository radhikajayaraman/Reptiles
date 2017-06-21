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
global data, sum_c,sum_actual_cost,total_actual_cost
print "Result,Enabled_value,Channel_name,Region_name,Input_Command"
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
    output = commands.getoutput(command_str)
#    print output
    try:
        data = json.loads(output)
    except ValueError:
        continue


    # fetching fields from input command
    def inputs_from_cmd():
        # fetching gender
        r = re.compile('-g (.*?) -r')
        g = r.search(command_str)
        if g:
            gender_in = str(g.group(1))
            #print gender_in
        # fetching category
        s = re.compile('-c(.*?)-m')
        c = s.search(command_str)
        if c:
            category_in = c.group(1)
            #print category_in
        # fetching profile
#	t = re.compile('-m (.*?) -p')
        t = re.compile('-m "(.*?)" -p')
        p = t.search(command_str)
        if t:
            profile_in = str(p.group(1))
#            print profile_in
        # fecthing budget
        u = re.compile('-b(.*?)$')
        b = u.search(command_str)
        if u:
            budget_in = b.group(1)
            #print budget_in
        return gender_in,category_in,profile_in,budget_in
    def enabled_value_from_mongo(region_name,channel_name):
	mongo_entire = db.channel_mappings.find({})
	for ena in mongo_entire:
            Enab = (ena['region'] + ',', ena['channel_name'] + ',', ena['enabled'])
            region_m = Enab[0][:-1]
            channel_m = Enab[1][:-1]
            if region_name == region_m and channel_name == channel_m:
                return Enab[2]
    def del_channel_check():
	for i in range(0, len(data['package']['region'])):
	    if data['package']['region'][i]['channel_order'] == []:
                continue
            else:
                for j in range(0, len(data['package']['region'][i]['channels'])):
                    channel_name = data['package']['region'][i]['channels'][j]['channel_name']
                    region_name = data['package']['region'][i]['region_name']
		    if region_name == "National":
			enabled_value = enabled_value_from_mongo(region_name,channel_name)
			#print repr(enabled_value)
			if enabled_value == None:
			    enabled_value = enabled_value_from_mongo("DTH",channel_name)
			    #print repr(enabled_value)
			    if enabled_value == 1:
				return enabled_value,channel_name,region_name,True
			    else:
				return enabled_value,channel_name,region_name,False
		    elif region_name != "National":
			enabled_value = enabled_value_from_mongo(region_name,channel_name)
			#print repr(enabled_value)
			if enabled_value == 1:
			    return enabled_value,channel_name,region_name,True
			else: 
			    return enabled_value,channel_name,region_name,False
    ena,chan,reg,result = del_channel_check()
    if  result == True:
	print "Pass",',',ena,',',chan,',',reg,',',
    else: 
	print "Fail",',',ena,',',chan,',',reg,',',
    print input_command
