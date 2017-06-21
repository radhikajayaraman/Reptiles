from pymongo import MongoClient
import toml
import logging
import random
import os
import time
import commands
import json


with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())

mongo_client = MongoClient(config["app"]["mongo_conn_str"])

# Connect to DB
db = mongo_client.dsp

# get all regions
regions = list(db.regions.distinct("region"))
genders = ['Male', 'Female', 'Male,Female']
spot_duration = [10, 20, 30]
ages = ["30+", "22+", "15-21", "22-30", "50+", "22-40", "09-21", "04-14", "15+"]

print "Budget_given,package_cost,budget_diff,status,Input_Command"
#path = "/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix_algs/mix-algs/media_packages/"
path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
for cnt in range(0, 3000):

    reg_iter = random.sample(range(0, len(regions)-1), random.randint(1, len(regions)-1))
    current_regions = []
    for i in reg_iter:
        current_regions.append(regions[i])
    current_regions_str = '\"' + ','.join(current_regions) + '\"'




    age_str = '\"' + ages[random.randint(0, len(ages)-1)] + '\"'
    gender_str = '\"' + genders[random.randint(0, len(genders)-1)] + '\"'
    cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
    command_str = "python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16" + " -a " + age_str + " -g " + gender_str + \
                  " -r "  + current_regions_str +  cat_prof + " -p " + \
                  str(random.randint(5, 20)) + " -s " + str(spot_duration[random.randint(0, 2)]) + " -b " + \
                  str(random.randint(0, 1000000))

    input_command = command_str.replace(',',' ')
    #to fetch the last value of the command line as the value is dynamic
    budget_all = command_str.split(' ')
    budget = budget_all[-1]
    output = commands.getoutput(command_str)
    #print output
    data = json.loads(output)
    discounted_package_cost = data['package']['discounted_package_cost']
    package_cost = data['package']['package_cost']
    budget_diff = int(budget) - int(package_cost)
    print budget + ',',
    print package_cost,
    print ',',budget_diff,
    if budget_diff >= 0:
        print ',LESS,',
    else:
        print ',MAX,',
    print input_command

