from __future__ import division
from pymongo import MongoClient
import toml
import logging
import random
import os
import time
import commands
import json
print "Result_Discount,Result_bud_overshoot,Result_actual_cost,Result_Cost,Discount_Percentage,Budget_shoot_status,Actual_cost_computed,Actual_cost_response,Type,total_cost,package_cost,Budget_input,Budget_Difference,Discount,input_command,cost,cost_r"

global actual_cost_computed, res, res2 ,res3 , res1,type_r,channel_r,d,p,status,a,aa,actual_cost_r,total_cost,package_cost,budget_input,budget_diff,discount,input_command,rotates
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp
regions = list(db.regions.distinct("region"))
genders = ['Male', 'Female', 'Male,Female']
#spot_duration = [10, 20, 30]
spot_duration = [15,25]
#path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/"
for cnt in range(0, 3000):
    reg_iter = random.sample(range(0, len(regions)-1), random.randint(1, len(regions)-1))
    current_regions = []
    for i in reg_iter:
        current_regions.append(regions[i])
    current_regions_str = '\"' + ','.join(current_regions) + '\"'
    gender_str = '\"' + genders[random.randint(0, len(genders) - 1)] + '\"'
    cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
    command_str = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " + gender_str +  \
              " -r "  + current_regions_str +   cat_prof +" -p " + str(random.randint(5,30)) + " -s " + str(spot_duration[random.randint(0,1)]) + " -b "  + str(random.randint(0,3000000))
#    print command_str
    input_command = command_str.replace(',', ' ')
    budget_all = command_str.split(' ')
    budget_input = budget_all[-1]
    output = commands.getoutput(command_str)
    try:
        data = json.loads(output)
    except ValueError:
        continue
#for r in data:
    if data['package']['region'][0]['region_cost'] is 0:
        continue
    total_cost = data['package']['total_cost']
    package_cost = data['package']['package_cost']
    type_r = data['package']['region'][0]['channels'][0]['type']
    #print type_r
    channel_r = data['package']['region'][0]['channels'][0]['channel_name']
    rotates_r = data['package']['region'][0]['channels'][0]['rotates']
    cost_r = data['package']['region'][0]['channels'][0]['cost']
    spot_dur_r = data['package']['spot_duration']
    region_r = data['package']['region'][0]['region_name']
    ## DISCOUNT Calculation
    discount = int(total_cost)-int(package_cost)
    discount_percentage = (abs(discount) *100 ) / int(total_cost)
    d = round(discount_percentage,2)
    if discount_percentage <= 15:
        res = "Pass"
    else:
        res = "Fail"
    ### BUDGET OVERSHOOT Calculation
    budget_diff = int(budget_input) - int(package_cost)
    if budget_diff >= 0:
        percent = (abs(budget_diff)*100) / int(budget_input)
        p = round(percent,2)
        if percent <= 5:
            res1 = "Pass"
        elif percent >= 5:
            res1 = "Fail"
        status = "budget undershoot % is "
    elif budget_diff <= 0:
        percent = (abs(budget_diff)*100) / int(budget_input)
        p = round(percent,2)
        if percent <= 5:
            res1 = "Pass"
        elif percent >= 5:
            res1 = "Fail"
        status = "budget overshoot % is "
        ###Actual cost computation
        #fetching the ER from mongo
        mongo_entire = db.effective_rates.find()
        for rates in mongo_entire:
            #Erate = []
            Erate = (rates['region'] + ',', rates['channel'] + ',', rates['effective_rate'])
            for i in enumerate(Erate):
                region_m = Erate[0][:-1]
                channel_m = Erate[1][:-1]
                if (region_r == region_m and channel_r == channel_m) or (type_r == region_m and channel_r == channel_m):
                    E_value = Erate[2]
                    #computing actual cost
                    actual_cost_computed =round(int(E_value) * (int(spot_dur_r) / 10))
		    #actual_cost_computed = round(E_value * ((spot_dur_r) / 10))
                    a = "Actual_cost_computed "
        #Comparing actual cost from response and computation
                    actual_cost_r = data['package']['region'][0]['channels'][0]['actual_cost']
                    aa = "Actual_cost_response "
                    if type_r == "Spliced":
                        if actual_cost_r == actual_cost_computed:
                            res2 = "Pass"
                            #Check cost field for spliced channel
                            cost = actual_cost_computed * int(rotates_r)
                            if cost == cost_r:
                                res3 = "Pass"
                            else:
                                res3 = "Fail"
                        else:
                            res2 = "Fail"
                    elif type_r == "Regional" or type_r == "National":
                        if actual_cost_r >= (0.96 * actual_cost_computed) and actual_cost_r <= (1.25 * actual_cost_computed):
                            res2 = "Pass"
                            #check the cost field for regional or national channel
                            cost = actual_cost_r * int(rotates_r)
                            min = round(0.96 * int(cost))
                            max = round(1.25 * int(cost))
                            if cost >= int(min) and cost <= int(max):
                                res3 = "Pass"
                            else:
                                res3 = "Fail"
                        else:
                            res2 = "Fail"
    print res,',',res1,',', res2, ',',res3 ,',',d,',',status+str(p),',',a+str(actual_cost_computed),',',aa+str(actual_cost_r),',',type_r,',',total_cost,',',package_cost,',',budget_input,',',budget_diff,',',discount,',',input_command,',',cost,',',cost_r

