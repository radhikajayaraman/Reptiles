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
global data, sum_c, g

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
#region from mongo one by one
mongo_entire = db.effective_rates.find()
# storing the values of region, channels and effective rate in Erate list
for rates in mongo_entire:
    Erate = []
    Erate = (rates['region'] +',',rates['channel'] +',',rates['effective_rate'])
    #print "Printing entire line from table",Erate
# Picking the regions from table one by one to pass as input
    for i, val in enumerate(Erate):
        #[:-1] is used to remove the last character comma from the variable
        region = Erate[0][:-1]
        reg = '\"'+ region + '\"'

#path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/"
##Number of iterations
        for i in range(0,25):
            cat_prof = random.choice(list(open('imp_cat_prof_map.txt'))).rstrip()
            gen = '\"' + random.choice(genders) + '\"'
            reg_iter = random.sample(range(0, len(regions) - 1), random.randint(1, len(regions) - 1))
            current_regions = []
            for j in reg_iter:
                current_regions.append(regions[j])
                current_regions_str = '\"' + ','.join(current_regions) + '\"'
                command_str = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " + gen + \
                  " -r " + reg + cat_prof + " -p " + str(random.randint(7,10)) + " -s " + str(
        spot_duration[random.randint(0, 1)]) + " -b " + str(random.randint(10000,15000))
    print command_str
    output = commands.getoutput(command_str)
    print output
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

    def tvt_from_channel_tvt(region_out,gender_out,age_out,channel_out):
        mongo_entire = db.channel_tvt.find()
        for tv in mongo_entire:
            full = (tv['region'] + ',', tv['gender'][0] + ',', tv['age'] + ',', tv['channel'] + ',',tv['tvt'])
            #print full
            if region_out == full[0][:-1] and gender_out == full[1][:-1] and age_out == full[2][:-1] and channel_out == full[3][:-1]:
                tvt = full[4][:-1]
                tvt_final = tvt * 1000
                return tvt_final

    def percent_from_reach_split(region_out):
        mongo_entire = db.reach_split.find()
        for res in mongo_entire:
            full = (res['region'] + ',', res['cable_percent'] + ',', res['dth_percent'])
            if region_out ==  full[0][:-1]:
                cable_p = full[1][:-1]
                dth_p = full[2][:-1]
                return cable_p,dth_p

    def impressions():
        ge,c,p,b = inputs_from_cmd()
        profile = p
        #print profile
        gender_out = data['package']['gender']
	gend = '\"'+gender_out+'\"'
        #print gender_out
        if '\"'+ gender_out +'\"' == '"Female"':
            g = 'F'
            audience_type =  '\"' + profile +' ' + g + '\"'
        elif '\"'+ gender_out +'\"' == '"Male"':
            g = 'M'
            audience_type = '\"' + profile +' '+ g + '\"'
            age_from_mongo = age_from_profile_to_tg(audience_type)
	    #age_from_mongo =  age_from_profile_to_tg("Value conscious M")
	    print age_from_mongo
	    age = '\"'+age_from_mongo+'\"'
            for i in range(0, len(data['package']['region'])):
                if data['package']['region'][i]['channel_order'] == []:
                    continue
                else:
                    impr = 0
                    for j in range(0, len(data['package']['region'][i]['channels'])):
                        region_o = data['package']['region'][i]['region_name']
			region_out = '\"'+region_o+'\"'
                        print region_out
                        channel_o = data['package']['region'][i]['channels'][j]['channel_name']
			channel_out = '\"'+channel_o+'\"'
                        print channel_out
                        type_out = data['package']['region'][i]['channels'][j]['type']
                        print type_out
                        rotates = data['package']['region'][i]['channels'][j]['rotates']
                        print rotates
                        imp_out = data['package']['region'][i]['region_impressions']
                        print imp_out
			print gender_out, age
			tvt = tvt_from_channel_tvt(region_out,gend,age,channel_out)
			print tvt
                        cable_p,dth_p = percent_from_reach_split(region_out)
                        if type == "Regional" and type == "National":
                            imp = tvt * rotates
                            impr +=imp
                            if impr == imp_out:
                                return True
                            else:
                                return False



    imp = impressions()
    if imp == True:
        print "Pass"
    else:
        print "Fail"
