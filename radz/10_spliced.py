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
global data, sum_c, g, input_command

##config file
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp
##inputs for the command
genders = ['Male', 'Female']
regions = list(db.regions.distinct("region"))
spot_duration = [10, 20]
#path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/"
for z in range(0,500):
    mongo_entire = db.regions.find()
    for regs in mongo_entire:
        regg = []
        regg = (regs['region'] + ',', regs['contained_in'] + ',', regs['tooltip'] + ',', regs['location'] + ',', regs['type'])
        for n, val in enumerate(regg):
            region = regg[0][:-1]
            reg = '\"'+ region + '\"'
            for i in range(0,1000):
                cat_prof = random.choice(list(open('imp_cat_prof_map.txt'))).rstrip()
                gen = '\"' + random.choice(genders) + '\"'
                command_str = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " + gen + \
                     " -r " + reg + cat_prof + " -p " + str(random.randint(7,10)) + " -s " + str(spot_duration[random.randint(0, 1)]) + " -b  " + str(random.randint(0 , 7000))
                output = commands.getoutput(command_str)
                input_command = command_str.replace(',', ' ')
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
        t = re.compile('-m "(.*?)" -p')
        p = t.search(command_str)
        if t:
            profile_in = p.group(1)
            #print profile_in
        # fecthing budget
        u = re.compile('-b(.*?)$')
        b = u.search(command_str)
        if u:
            budget_in = b.group(1)
            #print budget_in
        return gender_in,category_in,profile_in,budget_in

    def er_from_mongo(region_name,channel_name):
        # actual_cost from mongo
        mongo_entire = db.effective_rates.find()
        for rates in mongo_entire:
            #print rates
            Erate = (rates['region'] + ',', rates['channel'] + ',', rates['effective_rate'])
            region_m = Erate[0][:-1]
            channel_m = Erate[1][:-1]
            if region_name == region_m and channel_name == channel_m:
                return Erate[2]

    def ten_spliced():
        for i in range(0,len(data['package']['region'])):
            ig = "ignore"
            if data['package']['region'][i]['channel_order'] == []:
                continue
                #If channel_order is not empty, then compute the actual cost
            if len(data['package']['region'][i]['channel_order']) > 1:
                return ig
            else:
                region_name = data['package']['region'][i]['region_name']
                for j in range(0,len(data['package']['region'][i]['channels'])):
                    type_out = data['package']['region'][i]['channels'][j]['type']
                    if type_out == 'Spliced':
                        channel_name = data['package']['region'][i]['channels'][j]['channel_name']
                        actual_cost_out = data['package']['region'][i]['channels'][j]['actual_cost']
                        rotates_out = data['package']['region'][i]['channels'][j]['rotates']
			spot_duration = data['package']['spot_duration']
                        er_fr_mongo = er_from_mongo(region_name, channel_name)
                        if er_fr_mongo == None and region_name == "National":
                            er_fr_mongo = er_from_mongo("DTH",channel_name)
                            actual_cost_computed = int(er_fr_mongo) * int(rotates_out) * (int(spot_duration)/10)
                            if actual_cost_out < (1.1 * actual_cost_computed):
                                print "ER",er_fr_mongo,"rotates",rotates_out,"actual_cost_out",actual_cost_out,"actual_cost_computed",actual_cost_computed
                                return True
                            else:
                                print "ER",er_fr_mongo,"rotates",rotates_out,"actual_cost_out",actual_cost_out,"actual_cost_computed",actual_cost_computed
                                return False
                        else:
                            actual_cost_computed = int(er_fr_mongo) * int(rotates_out) * (int(spot_duration)/10)
                            if actual_cost_out < (1.1 * actual_cost_computed):
                                print "ER",er_fr_mongo,"rotates",rotates_out,"actual_cost_out",actual_cost_out,"actual_cost_computed",actual_cost_computed
                                return True
                            else:
                                print "ER",er_fr_mongo,"rotates",rotates_out,"actual_cost_out",actual_cost_out,"actual_cost_computed",actual_cost_computed
                                return False
                    else:
                        return ig
	
    ten_spli = ten_spliced()
    if ten_spli == True:
        print "Pass",',',
    elif ten_spli == False:
        print "Fail",',',
    else:
        print "Ignore",',',
    print input_command
