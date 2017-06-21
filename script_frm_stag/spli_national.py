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
#print "Tax,Gender,Budget_Shoot,Budget_diff_percentage,Result_Cost,Result_Discount,Result_Cutoff,Input_command"
print "Result_impression, Impression_from_response,Impression_calcltd,Input_command"
##config file
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp
##inputs for the command
genders = ['Male', 'Female', 'Male,Female']
#regions = list(db.regions.distinct("region"))
region = ['National']
spot_duration = [10,15,20,25,30]
#path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/"
##Number of iterations
for i in range(0,50):
    cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
    gen = '\"' + random.choice(genders) + '\"'
    command_str = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " + gen + \
                  " -r 'National'" + cat_prof + " -p " + str(random.randint(5, 99)) + " -s " + str(
        spot_duration[random.randint(0, 4)]) + " -b " + str(random.randint(300000, 1000000))
#    print command_str
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
            else:
                region_name = data['package']['region'][i]['region_name']
                for j in range(0,len(data['package']['region'][i]['channels'])):
                    type_out = data['package']['region'][i]['channels'][j]['type']
		    if type_out == 'National':
			continue
                    elif type_out == 'Spliced':
                        channel_name = data['package']['region'][i]['channels'][j]['channel_name']
                        actual_cost_out = data['package']['region'][i]['channels'][j]['cost']
                        rotates_out = data['package']['region'][i]['channels'][j]['rotates']
			spot_duration = data['package']['spot_duration']
                        er_fr_mongo = er_from_mongo(region_name, channel_name)
                        if er_fr_mongo == None and region_name == "National":
                            er_fr_mongo = er_from_mongo("DTH",channel_name)
                            actual_cost_computed = int(er_fr_mongo) * int(rotates_out) * (int(spot_duration)/10)
                            if actual_cost_out == (int(actual_cost_computed / 1.1)):
                                #print "ER",er_fr_mongo,"rotates",rotates_out,"actual_cost_out",actual_cost_out,"actual_cost_computed",actual_cost_computed
                                return True, er_fr_mongo,rotates_out,actual_cost_out,actual_cost_computed
                            else:
                                #print "ER",er_fr_mongo,"rotates",rotates_out,"actual_cost_out",actual_cost_out,"actual_cost_computed",actual_cost_computed
                                return False, er_fr_mongo,rotates_out,actual_cost_out,actual_cost_computed
                        else:
                            actual_cost_computed = int(er_fr_mongo) * int(rotates_out) * (int(spot_duration)/10)
                            if actual_cost_out == (int(actual_cost_computed / 1.1)):
                                #print "ER",er_fr_mongo,"rotates",rotates_out,"actual_cost_out",actual_cost_out,"actual_cost_computed",actual_cost_computed
                                return True, er_fr_mongo,rotates_out,actual_cost_out,actual_cost_computed
                            else:
                                #print "ER",er_fr_mongo,"rotates",rotates_out,"actual_cost_out",actual_cost_out,"actual_cost_computed",actual_cost_computed
                                return False, er_fr_mongo,rotates_out,actual_cost_out,actual_cost_computed
                    else:
                        return ig,"Null","Null","Null","Null"
	
    ten_spli, er, rota, ac_out, ac_comp = ten_spliced()
    if ten_spli == True:
        print "Pass",',',input_command,',',er,',',rota,',',ac_out,',',ac_comp
    elif ten_spli == False:
        print "Fail",',',input_command,',',er,',',rota,',',ac_out,',',ac_comp
    else:
        print "Ignore",',',input_command
