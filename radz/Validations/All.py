from pymongo import MongoClient
import toml
import logging
import random
import os
import time
import commands
import json
print "Result_Discount,Result_bud_overshoot,Discount_Percentage,Budget_shoot_status,total_cost,package_cost,Budget_input,Budget_Difference,Discount,input_command"
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp
regions = list(db.regions.distinct("region"))
genders = ['Male', 'Female', 'Male,Female']
spot_duration = [10, 20, 30]
path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
#path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix_algs/mix-algs/media_packages/"
for cnt in range(0, 6000):
    reg_iter = random.sample(range(0, len(regions)-1), random.randint(1, len(regions)-1))
    current_regions = []
    for i in reg_iter:
        current_regions.append(regions[i])
    current_regions_str = '\"' + ','.join(current_regions) + '\"'
    gender_str = '\"' + genders[random.randint(0, len(genders) - 1)] + '\"'
    cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
    command_str = " python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+"  " -g " + gender_str +  \
              " -r "  + current_regions_str +   cat_prof +" -p " + str(random.randint(5,20)) + " -s " + str(spot_duration[random.randint(0,2)]) + " -b "  + str(random.randint(0,1000000))
    print command_str
    input_command = command_str.replace(',', ' ')
    budget_all = command_str.split(' ')
    budget_input = budget_all[-1]
    output = commands.getoutput(command_str)
    try:
        data = json.loads(output)
    except ValueError:
        continue

    total_cost = data['package']['total_cost']
    package_cost = data['package']['package_cost']
    ## DISCOUNT Calculation
    discount = int(total_cost)-int(package_cost)
    discount_percentage = (abs(discount) *100 ) / int(total_cost)
    if discount_percentage <= 15:
        res = "Pass"
    else:
        res = "Fail"
    ### BUDGET OVERSHOOT Calculation
    budget_diff = int(budget_input) - int(package_cost)
    if budget_diff >= 0:
        percent = (abs(budget_diff)*100) / int(budget_input)
        if percent <= 5:
            res1 = "Pass"
        elif percent >= 5:
            res1 = "Fail"
        status = "budget undershoot % is "
    elif budget_diff <= 0:
        percent = (abs(budget_diff)*100) / int(budget_input)
        if percent <= 5:
            res1 = "Pass"
        elif percent >= 5:
            res1 = "Fail"
        status = "budget overshoot % is "
    print res,',',res1,',',discount_percentage,',',status+str(percent),',',total_cost,',',package_cost,',',budget_input,',',budget_diff,',',discount,',',input_command
