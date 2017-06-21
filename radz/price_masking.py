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
global data, sum_c,sum_actual_cost,total_actual_cost,input_command
#print "Tax,Gender,Budget_Shoot,Budget_diff_percentage,Result_Actl_Cost,Actl_Cost_Mongo,Actl_Cost_Response,Result_Cost,Result_Discount,Result_Cutoff,Input_command"
#print "Budget_shoot,Budget_diff_percentage,Input_budget,Response_budget,inp_cmd"
#print "Result_ApportioningER,Calculated_AC,Algo_Response_AC,Input_Cmd"
#print "Budget_shoot,bud_diff_percentage,bud_diff_figure,bud_in,bud_out,Input_command"
print "Result_price_masking,Input_command,Computed_val,Actual_cost_out"
##config file
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp
##inputs for the command
genders = ['Male', 'Female', 'Male,Female']
regions = list(db.regions.distinct("region"))
reg_1 = ['Bangalore','Delhi NCR','Orissa','Mumbai','Rajasthan','Madhya Pradesh','Kerala']
#spot_duration = [10]
#path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/"
##Number of iterations
for i in range(0,100):
    mongo_entire = db.regions.find()
    for regs in mongo_entire:
        regg = []
        regg = (regs['region'] + ',', regs['contained_in'] + ',', regs['tooltip'] + ',', regs['location'] + ',', regs['type'])
        for n, val in enumerate(regg):
            region = regg[0][:-1]
	    if region == "National":
		continue
	    else:
            	reg = '\"'+ region + '\"'
	    	cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
	    	gen = '\"' + random.choice(genders) + '\"'
		re = '\"' +random.choice(reg_1) + '\"' 
	    	command_str = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " + gen + \
                  " -r " + re + cat_prof + " -p " + str(random.randint(5, 99)) + " -s 10 " " -b " + str(random.randint(0,9000))
    		input_command = command_str.replace(',', ' ')
		#print input_command
    		output = commands.getoutput(command_str)
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

    def price_masking_check():
	for i in range(0, len(data['package']['region'])):
	    if data['package']['region'][i]['channel_order'] == []:
		continue
	    else:
		region_name =  data['package']['region'][i]['region_name']
		for j in range(0, len(data['package']['region'][i]['channels'])):
		    type_out = data['package']['region'][i]['channels'][j]['type']
		    if type_out != "Spliced":
			continue
		    else:
			actual_cost_out = data['package']['region'][i]['channels'][j]['actual_cost']
			rotates_out = data['package']['region'][i]['channels'][j]['rotates']
			channel_name = data['package']['region'][i]['channels'][j]['channel_name']
			er = er_from_mongo(region_name,channel_name)
			if region_name == "National" and er == None :
			    er = er_from_mongo("DTH",channel_name)
			    calc = int(er) * int(rotates_out) * 1.1
			    if actual_cost_out < calc:
                                return True,calc,actual_cost_out
                            else:
                                return False,calc,actual_cost_out
			else:
			    calc = int(er) * int(rotates_out) * 1.1
			    if actual_cost_out < calc:
				return True,calc,actual_cost_out
			    else:
				return False,calc,actual_cost_out
    price_mask,computed_val,act_cost = price_masking_check()
    if price_mask == True:
	print "Pass",',',computed_val,',',act_cost,',',
    else:
	print "Fail",',',computed_val,',',act_cost,',',
    print input_command 
			 
