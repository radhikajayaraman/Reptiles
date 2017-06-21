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

global data, sum_c, region_name

##config file
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.mix
##inputs for the command
genders = ['Male', 'Female', 'Male,Female']
regions = list(db.regions.distinct("region"))
spot_duration = [10, 15, 20, 25, 30]
# path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/"
##Number of iterations
for i in range(0, 100):
    # for i in range(0,1000):
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
    output = commands.getoutput(command_str)
    #print command_str
    #print output
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
            # print gender_in
        # fetching category
        s = re.compile('-c(.*?)-m')
        c = s.search(command_str)
        if c:
            category_in = c.group(1)
            # print category_in
        # fetching profile
        t = re.compile('-m (.*?) -p')
        p = t.search(command_str)
        if t:
            profile_in = str(p.group(1))
        # print profile_in
        # fecthing budget
        u = re.compile('-b(.*?)$')
        b = u.search(command_str)
        if u:
            budget_in = b.group(1)


    def cutoff_from_mongo(region_name, channel_name):
        # cutoff_rate from mongo
        mongo_entire = db.effective_rates.find({})
        for rates in mongo_entire:
            # print rates
            Erate = (rates['region'] + ',', rates['channel'] + ',', rates['cutoff_rate'])
            region_m = Erate[0][:-1]
            channel_m = Erate[1][:-1]
            if region_name == region_m and channel_name == channel_m:
                return Erate[2]


    def cutoff_rate_check():
        final_cost_compute = 0
        # cutoff_rate from mongo
        for i in range(0, len(data['package']['region'])):
            #print 'i',i
            if data['package']['region'][i]['channel_order'] == []:
                continue
                # If channel_order is not empty, then compute the actual cost
            else:
                sum_c = 0
                for j in range(0, len(data['package']['region'][i]['channels'])):
                    #print 'j',j
                    channel_name = data['package']['region'][i]['channels'][j]['channel_name']
                    type_out = data['package']['region'][i]['channels'][j]['type']
                    region_name = data['package']['region'][i]['region_name']
                    if region_name == 'National' and (type_out == 'National' or type_out == 'Regional'):
                        region_name = data['package']['region'][i]['region_name']
                    elif region_name == 'National' and type_out == 'Spliced':
                        region_name = 'DTH'
                    else:
                        region_name = data['package']['region'][i]['region_name']
                    E_value = cutoff_from_mongo(region_name, channel_name)
                    #print E_value
                    spot_duration = data['package']['spot_duration']
                    actual_compute = E_value * (spot_duration / 10)
                    rotates_out = data['package']['region'][i]['channels'][j]['rotates']
                    cost_compute = actual_compute * rotates_out
                    #print 'region_name', region_name, 'channel_name', channel_name, 'type', type_out, 'E_value', E_value, 'actual_compute', actual_compute, 'rotates', rotates_out, 'cost_compute', cost_compute
                    sum_c += cost_compute
                    #print 'sum_c', sum_c
            final_cost_compute += sum_c
            #print 'final', final_cost_compute
        #print 'minimum_package_cost', data['package']['minimum_discounted_cost']
	min_pakg_cost = data['package']['minimum_discounted_cost']
	final  = round(final_cost_compute)
	print 'Min_package_cost',',',min_pakg_cost,',','Final_computed',',',final,',', 
        if final == min_pakg_cost or min_pakg_cost <= (final - 1) or min_pakg_cost >= (final + 1)  :
            return True
        else:
            return False


    cut_off = cutoff_rate_check()
    if cut_off == True:
        print "Pass"
    else:
        print "False"
