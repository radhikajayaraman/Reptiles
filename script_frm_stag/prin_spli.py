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
global data, sum_c,sum_actual_cost,total_actual_cost,input_command
#print "Tax,Gender,Budget_Shoot,Budget_diff_percentage,Result_Actl_Cost,Actl_Cost_Mongo,Actl_Cost_Response,Result_Cost,Result_Discount,Result_Cutoff,Input_command"
#print "Budget_shoot,Budget_diff_percentage,Input_budget,Response_budget,inp_cmd"
#print "Result_ApportioningER,Calculated_AC,Algo_Response_AC,Input_Cmd"
#print "Budget_shoot,bud_diff_percentage,bud_diff_figure,bud_in,bud_out,Input_command"
#print "Result_10_spliced,Input_command,ER_mongo,Rotates,actual_cost_out,actual_cost_computed"
print "Region_name,channel_name,ER_from_mongo,Rotates,spot_duration,Type,actual_cost_out,inp_cmd"
##config file
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp
##inputs for the command
genders = ['Male', 'Female', 'Male,Female']
spot_duration = [10,15,20,25,30]
regions = ['Bangalore','Kerala','Delhi NCR','Hyderabad','Maharashtra/Goa','Mumbai','Uttar Pradesh','TN/Pondicherry','West Bengal','North East']
#path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/"
##Number of iterations
for i in range(0,50):
    cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
    gen = '\"' + random.choice(genders) + '\"'
    reg = '\"' + random.choice(regions) + '\"'
    command_str = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " + gen + \
                  " -r " + reg + cat_prof + " -p " + str(random.randint(5, 99)) + " -s " + str(
        	spot_duration[random.randint(0, 4)]) + " -b " + str(random.randint(0,9000)) 
    input_command = command_str.replace(',', ' ')
		#print input_command
    output = commands.getoutput(command_str)
    try:
	data = json.loads(output)
    except ValueError:
	continue



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
            if data['package']['region'][i]['channel_order'] == []:
                continue
            else:
                region_name = data['package']['region'][i]['region_name']
                for j in range(0,len(data['package']['region'][i]['channels'])):
                    type_out = data['package']['region'][i]['channels'][j]['type']
                    channel_name = data['package']['region'][i]['channels'][j]['channel_name']
                    actual_cost_out = data['package']['region'][i]['channels'][j]['actual_cost']
                    rotates_out = data['package']['region'][i]['channels'][j]['rotates']
		    spot_duration = data['package']['spot_duration']
                    er_fr_mongo = er_from_mongo(region_name, channel_name)
                    if er_fr_mongo == None and region_name == "National":
                        er_fr_mongo = er_from_mongo("DTH",channel_name)
			print region_name,',',channel_name,',',er_fr_mongo,',',rotates_out,',',spot_duration,',',type_out,',',actual_cost_out,',',
		    else:
			print region_name,',',channel_name,',',er_fr_mongo,',',rotates_out,',',spot_duration,',',type_out,',',actual_cost_out,',',
    q = ten_spliced()	
    print input_command
