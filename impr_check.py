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

    def tvt_mongo_new(r, c, a, g):
	em = db.channel_tvt.find({"channel":c,"region":r,"gender":g,"age":a})
	for document in em:
	    result = document.get("tvt")
	    return result

    def val_reach_spli_mongo(region_name):
	vl = db.reach_split.find({"region":region_name})
	for doc in vl:
            if region_name == "National":
		return doc.get("dth_percent")
	    elif region_name != "National":
		return doc.get("cable_percent")
		 
    def impre():
	total_impr = 0
	for i in range(0,len(data['package']['region'])):
            if data['package']['region'][i]['channel_order'] == []:
                continue
                #If channel_order is not empty, then compute the actual cost
            else:
		sum_impr = 0
                region_name = data['package']['region'][i]['region_name']
                for j in range(0,len(data['package']['region'][i]['channels'])):
		    channel_name = data['package']['region'][i]['channels'][j]['channel_name']
		    age = data['package']['age']
		    gender = data['package']['gender']
		    if gender == 'Male,Female':
			g = ["Male","Female"]
		    elif gender == 'Male':
			g = ["Male"]
		    elif gender == 'Female':
			g = ["Female"]
		    type_out = data['package']['region'][i]['channels'][j]['type']
		    rotates_out = data['package']['region'][i]['channels'][j]['rotates']
		    tvt_from_mongo = tvt_mongo_new(region_name,channel_name,age,g)
		    tvt =  float(tvt_from_mongo) * 1000 * int(rotates_out)
		    print "tvt_frm_mongo",tvt_from_mongo,"rotates",rotates_out,"tvt",tvt,"regio",region_name,"cha",channel_name,"ge",g,"ty",type_out
		    if (region_name != 'National' and type_out == 'Spliced'):
			cable_value = val_reach_spli_mongo(region_name)
			impr = tvt * (cable_value / 100)
			print 'Impr_reg_spli',impr
		    elif (region_name != 'National' and type_out == 'Regional'):
			impr = tvt
			print 'Impr_reg_regio',impr
		    elif (region_name == 'National'):
			detail_reg_impr = []
			for key,value in data['package']['region'][i]['detailed_region_impressions'].items():
			    print key,value
			  

#		    if ((region_name  == "National" and type_out == "National") or (region_name != "National" and type_out == "Regional")):
#			impr = tvt
#			print "impr",impr
#		    elif (region_name == "National" and type_out == "Spliced"):
#			DTH_value = val_reach_spli_mongo(region_name)
#			print "DTH",DTH_value
#			impr = tvt * (DTH_value / 100)
#			print "impr", impr
#		    sum_impr += impr
#		    region_impression = data['package']['region'][i]['region_impressions']
#		    print "sum",sum_impr,"reg_imp",region_impression
#	    total_impr += sum_impr
#	impr_out = data['package']['package_impressions']
#	if impr_out == (round(total_impr)) or impr_out == ((round(total_impr) - 1)) or impr_out == (round(total_impr) + 1):
#	    return True, impr_out, round(total_impr)
#	else:
#	    return False, impr_out, round(total_impr)
#
    impr = impre()
#    imp_res, imp_response, imp_calculated = impre()
#    if imp_res == True:
#	print "Pass",',',imp_response,',',imp_calculated,',',input_command
#    else: 
#	print "Fail",',',imp_response,',',imp_calculated,',',input_command
