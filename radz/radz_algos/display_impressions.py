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
global data, sum_c
#print "Tax,Gender,Budget_Shoot,Budget_diff_percentage,Result_Actl_Cost,Actl_Cost_Mongo,Actl_Cost_Response,Result_Cost,Result_Discount,Result_Cutoff,Input_command"
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
#    command_str = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " + gen + \
#                  " -r " + current_regions_str + cat_prof + " -p " + str(random.randint(5, 99)) + " -s " + str(
#        spot_duration[random.randint(0, 4)]) + " -b " + str(random.randint(300000, 1000000))
    command_str = "python /home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+ -g 'Female' -r 'Bangalore,Kerala,Mumbai' -c 'Hair Care' -m 'Early Professionals' -p 10 -s 10 -b 50000"
    input_command = command_str.replace(',', ' ')
#    command_str = "python /home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+ -g 'Female' -r 'Bihar, Kerala, Jharkhand, Orissa' -c 'Hair Care' -m 'Early Professionals' -p 7 -s 25 -b 411920"
#    print command_str
    output = commands.getoutput(command_str)
    inp = command_str.replace(',', ' ') 
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
	t = re.compile('-m (.*?) -p')
#        t = re.compile('-m "(.*?)" -p')
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
    def age_from_profile_to_tg(profile):
        mongo_entire = db.profile_to_tg.find()
        for ag in mongo_entire:
            # print rates
            full = (ag['tg'] + ',', ag['audience_type'])
            if profile == full[1][:-1]:
                age_full = full[0][:-1]
                #print age_full
                a = re.compile('/(.*?)/')
                b = a.search(age_full)
                if a:
                    age = b.group(1)
                    return age

    def display_impression():
	for i in range(0, len(data['package']['region'])):	
	    if data['package']['region'][i]['channel_order'] == []:
		region_name = data['package']['region'][i]['region_name']
		print 'reg_no_chal',',',region_name,',',
	    else:
		for j in range(0, len(data['package']['region'][i]['channels'])):
		    region_name = data['package']['region'][i]['region_name']
		    print 'reg_with_chal',',',region_name,',',
		    channel_name = data['package']['region'][i]['channels'][j]['channel_name']
		    type_out = data['package']['region'][i]['channels'][j]['type']
		    channel_reach = data['package']['region'][i]['channels'][j]['channel_reach']
		    region_impressions = data['package']['region'][i]['region_impressions']
		    gender_out = data['package']['gender']
		    print 'chanl_name',',',channel_name,',',
		    print 'type',',',type_out,',',
		    print 'region_imp',',',region_impressions,',',
		    rotates = data['package']['region'][i]['channels'][j]['rotates']
		    print 'rotates',',',rotates
		    gen,cat,profile,bud = inputs_from_cmd()
		    prof = '\"'+profile+'\"' 
		    #details required for mongo
		    if '\"'+ gender_out +'\"' == '"Female"':
			g = 'F'
            		audience_type =  '\"' + profile +' ' + g + '\"'
        	    elif '\"'+ gender_out +'\"' == '"Male"':
			g = 'M'
            		audience_type = '\"' + profile +' '+ g + '\"'
		    elif '\"'+gender_out+'\"' == '"Male,Female"':
			g = 'MF'
			audience_type = '\"' + profile +' '+ g + '\"'
			#age_from_mongo = age_from_profile_to_tg(audience_type)
			age_from_mongo = data['package']['age']
			print 'age',',',age_from_mongo,',',
			print 'profile',',',prof,',',
			print 'gen',',',gen,',',
			tot_imp = data['package']['package_impressions']
			print 'Total_impressions',',',tot_imp	    
#    print "Region_name without channels,Region_name with channels,Channel,Type,Region_impressions,Age,Gender,Inputcmd"
    disp = display_impression()
    print 'input',',',inp

    print "=====================================================================================================================================" 
