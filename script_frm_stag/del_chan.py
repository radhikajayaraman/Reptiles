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
regions = ['Bangalore','Kerala','Delhi NCR','Hyderabad','Maharashtra/Goa','Mumbai','Uttar Pradesh','TN/Pondicherry','West Bengal','North East']
spot_duration = [10,15,20,25,30]
#path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/"
##Number of iterations
for i in range(0,1000):
    cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
    gen = '\"' + random.choice(genders) + '\"'
    reg = '\"' + random.choice(regions) + '\"'
    command_str = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " + gen + \
                  " -r " + reg + cat_prof + " -p " + str(random.randint(5, 99)) + " -s " + str(
        spot_duration[random.randint(0, 4)]) + " -b " + str(random.randint(300000, 1000000))
    input_command = command_str.replace(',', ' ')
#    print input_command,',',
#    command_str = "python /home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+ -g 'Female' -r 'Bihar, Kerala, Jharkhand, Orissa' -c 'Hair Care' -m 'Early Professionals' -p 7 -s 25 -b 411920"
#    print command_str
    output = commands.getoutput(command_str)
#    print output
    try:
#	data = json.loads(output)
	data = json.loads('{"package": {"rating": 1.9655684576242554, "spot_duration": 20, "tax_amount": 74389, "package_name": "My Media Plan", "total_cost": 570314, "gender": "Female", "age": "09-21", "package_cost": 499300, "advance_payment_amount": 50000, "discounted_package_cost": 495925, "package_impressions": 1300625.873843262, "number_of_days": 12, "minimum_discounted_cost": 488220, "region": [{"channel_order": ["Zee News", "Sangeet Bangla", "Zee Cinema", "Colors", "Zee Bangla", "ETV News Bangla", "ET Now"], "combos": [], "region_name": "West Bengal", "universe": 4326594.540193736, "channels": [{"channel_cprp": 0, "secondages": 1080, "day_parts": [{"dispersion": 33.33, "day_part_name": "Morning", "rotates": 18, "day_part_definition": "0600-1200", "secondages": 360}, {"dispersion": 33.33, "day_part_name": "Afternoon", "rotates": 18, "day_part_definition": "1200-1800", "secondages": 360}, {"dispersion": 33.33, "day_part_name": "Evening", "rotates": 18, "day_part_definition": "1800-2400", "secondages": 360}], "channel_reach": 339193.4000000001, "channel_name": "Zee News", "cost": 17820, "rotates": 54, "type": "Spliced", "actual_cost": 12825}, {"channel_cprp": 0, "secondages": 480, "day_parts": [{"dispersion": 33.33, "day_part_name": "Morning", "rotates": 8, "day_part_definition": "0800-1200", "secondages": 160}, {"dispersion": 33.33, "day_part_name": "Afternoon", "rotates": 8, "day_part_definition": "1200-1800", "secondages": 160}, {"dispersion": 33.33, "day_part_name": "Evening", "rotates": 8, "day_part_definition": "1800-2300", "secondages": 160}], "channel_reach": 1113740.0, "channel_name": "Sangeet Bangla", "cost": 24288, "rotates": 24, "type": "Regional", "actual_cost": 22080}, {"channel_cprp": 0, "secondages": 700, "day_parts": [{"dispersion": 20.0, "day_part_name": "Morning", "rotates": 7, "day_part_definition": "0600-1030", "secondages": 140}, {"dispersion": 20.0, "day_part_name": "Mid-Morning", "rotates": 7, "day_part_definition": "1030-1330", "secondages": 140}, {"dispersion": 20.0, "day_part_name": "Afternoon", "rotates": 7, "day_part_definition": "1330-1600", "secondages": 140}, {"dispersion": 20.0, "day_part_name": "Evening", "rotates": 7, "day_part_definition": "1600-2000", "secondages": 140}, {"dispersion": 20.0, "day_part_name": "Night", "rotates": 7, "day_part_definition": "2000-2500", "secondages": 140}], "channel_reach": 962325.0, "channel_name": "Zee Cinema", "cost": 57750, "rotates": 35, "type": "Spliced", "actual_cost": 52500}, {"channel_cprp": 0, "secondages": 240, "day_parts": [{"dispersion": 75.0, "day_part_name": "Rest of day", "rotates": 9, "day_part_definition": "0900-1800", "secondages": 180}, {"dispersion": 25.0, "day_part_name": "Night", "rotates": 3, "day_part_definition": "1800-2400", "secondages": 60}], "channel_reach": 1061733.4000000001, "channel_name": "Colors", "cost": 44880, "rotates": 12, "type": "Spliced", "actual_cost": 40800}, {"channel_cprp": 0, "secondages": 240, "day_parts": [{"dispersion": 50.0, "day_part_name": "Rest of day", "rotates": 6, "day_part_definition": "0830-1700", "secondages": 120}, {"dispersion": 50.0, "day_part_name": "Evening", "rotates": 6, "day_part_definition": "1700-2400", "secondages": 120}], "channel_reach": 2225910.0, "channel_name": "Zee Bangla", "cost": 166980, "rotates": 12, "type": "Regional", "actual_cost": 151802}, {"channel_cprp": 0, "secondages": 900, "day_parts": [{"dispersion": 33.33, "day_part_name": "Morning", "rotates": 15, "day_part_definition": "0800-1200", "secondages": 300}, {"dispersion": 33.33, "day_part_name": "Afternoon", "rotates": 15, "day_part_definition": "1200-1800", "secondages": 300}, {"dispersion": 33.33, "day_part_name": "Evening", "rotates": 15, "day_part_definition": "1800-2400", "secondages": 300}], "channel_reach": 396610.0, "channel_name": "ETV News Bangla", "cost": 22770, "rotates": 45, "type": "Regional", "actual_cost": 20700}, {"channel_cprp": 0, "secondages": 480, "day_parts": [{"dispersion": 25.0, "day_part_name": "Rest of day", "rotates": 6, "day_part_definition": "0600-1700", "secondages": 120}, {"dispersion": 75.0, "day_part_name": "Night", "rotates": 18, "day_part_definition": "1700-2500", "secondages": 360}], "channel_reach": 0.0, "channel_name": "ET Now", "cost": 66240, "rotates": 24, "type": "Spliced", "actual_cost": 60218}], "region_cost": 400728, "discounted_region_cost": 364300, "region_impressions": 1292876.4941356927}, {"channel_order": ["Zee News", "IBN7"], "combos": [], "region_name": "National", "universe": 4326594.540193736, "detailed_region_impressions": {"West Bengal": 7749.873843261999}, "channels": [{"channel_cprp": 0, "secondages": 900, "day_parts": [{"dispersion": 33.33, "day_part_name": "Morning", "rotates": 15, "day_part_definition": "0600-1200", "secondages": 300}, {"dispersion": 33.33, "day_part_name": "Afternoon", "rotates": 15, "day_part_definition": "1200-1800", "secondages": 300}, {"dispersion": 33.33, "day_part_name": "Evening", "rotates": 15, "day_part_definition": "1800-2400", "secondages": 300}], "channel_reach": 33546.6, "channel_name": "Zee News", "cost": 99000, "rotates": 45, "type": "Spliced", "actual_cost": 90000}, {"channel_cprp": 0, "secondages": 900, "day_parts": [{"dispersion": 33.33, "day_part_name": "Morning", "rotates": 15, "day_part_definition": "0600-1200", "secondages": 300}, {"dispersion": 33.33, "day_part_name": "Afternoon", "rotates": 15, "day_part_definition": "1200-1800", "secondages": 300}, {"dispersion": 33.33, "day_part_name": "Evening", "rotates": 15, "day_part_definition": "1800-2400", "secondages": 300}], "channel_reach": 14649.300000000001, "channel_name": "IBN7", "cost": 49500, "rotates": 45, "type": "Spliced", "actual_cost": 45000}], "region_cost": 148500, "discounted_region_cost": 135000, "region_impressions": 7749.873843261999}]}}')
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
