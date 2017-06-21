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
print "Tax,Gender,Budget_Shoot,Budget_diff_percentage,Result_Actl_Cost,Actl_Cost_Mongo,Actl_Cost_Response,Result_Cost,Result_Disc_pakg_cost,Result_Discount,Result_Cutoff,Input_command"
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
    print command_str
    ##fields required from input given
    #budget_in =
    #profile =
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
            profile_in = str(p.group(1))
#            print profile_in
        # fecthing budget
        u = re.compile('-b(.*?)$')
        b = u.search(command_str)
        if u:
            budget_in = b.group(1)
            #print budget_in
        return gender_in,category_in,profile_in,budget_in
    def discounted_package_cost():
        sum_o = 0
        for i in range(0,len(data['package']['region'])):
            if data['package']['region'][i]['channel_order'] == []:
                continue
                #If channel_order is not empty, then compute the actual cost
            else:
                dis_reg_cost = data['package']['region'][i]['discounted_region_cost']
		#print dis_reg_cost
            sum_o += dis_reg_cost
            discounted_package_cost_out = data['package']['discounted_package_cost']
	    print 'sm_o',sum_o,'discpakgcost',discounted_package_cost_out
            if discounted_package_cost_out == sum_o:
                return True
            else:
                return False
    dis = discounted_package_cost()
    if dis == True:
	print 'Pass'
    else:
	print 'Fail'
