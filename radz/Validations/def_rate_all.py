from pymongo import MongoClient
import toml
import logging
import random
import os
import subprocess
import json
import time
import random
import commands
print "Result,Type,Computed_cost_min-Computed_cost_max,Package_cost,Input_Command"
#declaring global variables
global regions,channel_response,region_m,channel_m,total_cost,rotates,type
#Config 
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
#Mongo db
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
# Connect to DB
db = mongo_client.dsp
##########################
#Inputs needed for command
##########################
gender = random.choice(['Male', 'Female', 'Male,Female'])
regions = list(db.regions.distinct("region"))
spot_duration = [10, 20, 30]
########################
#Input Command
########################
path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
reg_iter = random.sample(range(0, len(regions)-1), random.randint(1, len(regions)-1))
for z in range(0, 3000):
    current_regions = []
for i in reg_iter:
    current_regions.append(regions[i])
    current_regions_str = '\"' + ','.join(current_regions) + '\"'
    cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
    command = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " "\""+ gender + "\"" \
              " -r "  "\"" + current_regions_str + "\""  +  cat_prof +" -p " + str(random.randint(5,20)) + " -s " + str(spot_duration[random.randint(0,2)]) + " -b "  + str(random.randint(0,1000000))
    input_command = command.replace(',',' ')
    output = commands.getoutput(command)
    try:
        data = json.loads(output)
    except Exception:
        continue

    #sregion = []
    region = data['package']['region'][0]['region_name']
    channels =[]
    channels = data['package']['region'][0]['channels'][0]['channel_name']
    type = []
    type = data['package']['region'][0]['channels'][0]['type']
    rotates = []
    rotates = data['package']['region'][0]['channels'][0]['rotates']
    discounted_package_cost = []
    discounted_package_cost = data['package']['discounted_package_cost']
    package_cost = data['package']['package_cost']
    rotates = data['package']['region'][0]['channels'][0]['rotates']
    type = data['package']['region'][0]['channels'][0]['type']
    mongo_entire = db.effective_rates.find()
    for rates in mongo_entire:
        Erate = []
        Erate = (rates['region'] +',',rates['channel'] +',',rates['effective_rate'])
        for i in enumerate(Erate):
            region_m = Erate[0][:-1]
            channel_m = Erate[1][:-1]
            E_value = Erate[2]
        if (region == region_m and channels == channel_m) or (type == region_m and channels == channel_m):
            Evalue = Erate[2]
            spot_dur = input_command[-1]
            if type == 'Spliced':
                computed_cost = int(E_value) * int(rotates) * (int(spot_dur)/10)
                if int(package_cost) == int(computed_cost):
                    print "Pass", ',',type,',',computed_cost,',',package_cost,',',command
                    break
                else:
                    print "Fail",',',type,',',computed_cost,',',package_cost,',',command
                    break
            elif type == 'National' or type == 'Regional':
                computed_cost_min = (int(E_value)*0.96) * int(rotates) * (int(spot_dur)/10)
                computed_cost_max = (int(E_value)*1.25) * int(rotates) * (int(spot_dur)/10)
                if package_cost >= computed_cost_min and package_cost <= computed_cost_max:
                    print "Pass",',',type,',',computed_cost_min,'-', computed_cost_max,',',package_cost,',',command
                    break
                else:
                    print "Fail",',',type,',',computed_cost_min,'-', computed_cost_max,',',package_cost,',',command
                    break


