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
global region_response,channel_response,region_m,channel_m,total_cost_response,rotates_response,type_response
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
duration = 10
spot_duration = 10
budget = 500 #Insufficient budget
########################
#Input Command
########################
path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"

for i in regions:
    cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
    command = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " "\""+ gender + "\"" \
              " -r "  "\"" + i + "\""  +  cat_prof +" -p " + str(duration) + " -s " + str(spot_duration) + " -b "  + str(budget)
        #print "Input command", command
#########################
#storing the output in out variable
#########################
    output = commands.getoutput(command)
        #print "Output:", output
##########################
#Storing the values from response
##########################
    try:
        data = json.loads(output)
    except Exception:
        continue
    region_response = data['package']['region'][0]['region_name']
    channel_response = data['package']['region'][0]['channels'][0]['channel_name']
    total_cost_response = data['package']['total_cost']
    discounted_package_cost = data['package']['discounted_package_cost']
    package_cost = data['package']['package_cost']
    rotates_response = data['package']['region'][0]['channels'][0]['rotates']
    type_response = data['package']['region'][0]['channels'][0]['type']
        #print region_response,channel_response,type_response

###########################
#Fetching effective rates from mongo
###########################
# get the entire table of effective rates
    mongo_entire = db.effective_rates.find()
# storing the values of region, channels and effective rate in Erate list
    for rates in mongo_entire:
        Erate = []
        Erate = (rates['region'] +',',rates['channel'] +',',rates['effective_rate'])
            #print "Printing entire line from table", Erate
# Picking the regions from table one by one to pass as input
        for i in enumerate(Erate):
            region_m = Erate[0][:-1]
            channel_m = Erate[1][:-1]
            E_value = Erate[2]
                #print region_m,channel_m,region_response,channel_response,type_response
            if region_response == region_m and channel_response == channel_m:
                    #print region_m,region_response,channel_m, channel_response,rotates_response,spot_duration
                E_value = Erate[2]
                    #print E_value
                    #print type_response
                if type_response == 'Spliced':
                    computed_cost = int(E_value) * int(rotates_response) * (int(spot_duration)/10)
                        #print "Type,Computed_cost, Discounted_package_cost,Package_cost",type_response,computed_cost,discounted_package_cost,package_cost
                        #print type_response,',',computed_cost,',',package_cost,',',
                    if int(package_cost) == int(computed_cost):
                        print "Pass", ',',type_response,',',computed_cost,',',package_cost,',',command
                        break
                    else:
                        print "Fail",',',type_response,',',computed_cost,',',package_cost,',',command
                        break
                elif type_response == 'National' or type_response == 'Regional':
                    computed_cost_min = (int(E_value)*0.96) * int(rotates_response) * (int(spot_duration)/10)
                    computed_cost_max = (int(E_value)*1.25) * int(rotates_response) * (int(spot_duration)/10)
                        #print "Type,Computed_cost_max,Computed_cost_min, Discounted_package_cost,Package_cost",type_response,computed_cost_max,computed_cost_min,discounted_package_cost,package_cost
                    if package_cost >= computed_cost_min and package_cost <= computed_cost_max:
                        print "Pass",',',type_response,',',computed_cost_min,'-', computed_cost_max,',',package_cost,',',command
                        break
                    else:
                        print "Fail",',',type_response,',',computed_cost_min,'-', computed_cost_max,',',package_cost,',',command
                        break
