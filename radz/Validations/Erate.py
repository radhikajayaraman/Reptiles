from pymongo import MongoClient
import toml
import logging
import random
import os
import subprocess
import json
import time

with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())

mongo_client = MongoClient(config["app"]["mongo_conn_str"])

# Connect to DB
db = mongo_client.dsp

# get all regions
regions = list(db.regions.distinct("region"))
genders = ['Male', 'Female', 'Male,Female']
spot_duration = 10
ages = ["30+", "22+", "15-21", "22-30", "50+", "22-40", "09-21", "04-14", "15+"]
#Insufficient budget to have jus one channel as output
budget = 500
duration = 10
profiles = list(db.profile_to_tg.distinct("audience_type"))
product_sub_cats = db.profile_to_brand.distinct('category')
# get the entire table of effective rates
mongo_entire = db.effective_rates.find()
# storing the values of region, channels and effective rate in Erate list
for rates in mongo_entire:
    Erate = []
    Erate = (rates['region'] +',',rates['channel'] +',',rates['effective_rate'])
    print "Printing entire line from table",Erate
# Picking the regions from table one by one to pass as input
    for i, val in enumerate(Erate):
        #[:-1] is used to remove the last character comma from the variable
        region = Erate[0][:-1]
        #channel_m = Erate[1]
        #E_value = Erate[2]
        #print E_value
        #print region_m
        #print channel_m
        #Values for the command
        age_str = '\"' + ages[random.randint(0, len(ages) - 1)] + '\"'
        gender_str = '\"' + genders[random.randint(0, len(genders) - 1)] + '\"'
        cat_str = '\"' + product_sub_cats[random.randint(0, len(product_sub_cats) - 1)] + '\"'
        profile_str = '\"' + profiles[random.randint(0, len(profiles) - 1)] + '\"'
        profile_str = profile_str.replace('MF', '')
        profile_str = profile_str.replace('M', '')
        profile_str = profile_str.replace('F', '')


        path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"
        for cnt in range(0,len(Erate)-1):
            #command_str = "python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16" + " -a " + age_str + " -g " + gender_str + \
                          #" -r " "\""+ region +"\"" " -c " + cat_str + " -m " + profile_str + " -p " + \
                      #str(duration) + " -s " + str(spot_duration) + " -b " + \
                     #str(budget)
            z = "\"Media\" -m \"Elders\""
            command_str = "python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16" + " -a " + age_str + " -g " + gender_str + \
                          " -r " "\""+ region +"\"" " -c " + z + " -p " + \
                      str(duration) + " -s " + str(spot_duration) + " -b " + \
                     str(budget)

            print "Input command", command_str
            response = subprocess.Popen(command_str,stdout=subprocess.PIPE, shell=True)
            out =  response.communicate()[0]
            print "Output:",out
            try:

                data = json.loads(out)
            except ValueError:
                print "Script crashed of bad input, so continuing to next"
                continue
            channel_r = data['package']['region'][0]['channel_order']
            print "Channel from response", channel_r
            region_r = data['package']['region'][0]['region_name']
            print "region from response", region
            type = data['package']['region'][0]['channels'][0]['type']
            print "Type from response", type
            rotates = data['package']['region'][0]['channels'][0]['rotates']
            print "Number of rotates from response",rotates
            spot_duration = data['package']['spot_duration']
            print "Number of spots from response",spot_duration
            Total_cost = data['package']['total_cost']
            print "Total cost from response", Total_cost

            for rates in mongo_entire:
                Erate = []
                Erate = (rates['region'] + ',', rates['channel'] + ',', rates['effective_rate'])

                for i, val in enumerate(Erate):
            # [:-1] is used to remove the last character comma from the variable
                    region_m = Erate[0][:-1]
                    channel_m = Erate[1][:-1]
                    E_value = Erate[2]
                    if region_r == region_m and channel_m == channel_r:
                        print "Region,channel from mongo:",region_m, channel_m
                        print "Region,channel from response :",region_r, channel_r
                    """"
                    if region_r == region_m and channel_m == channel_r:
                        print "Region_mongo, Region_response:",region_m,region_r
                        if type == "Spliced":
                            Cost_splice_channel = int(E_value) * int(rotates) * (int(spot_duration) /10)
                            print "Computed cost of the spliced channel", Cost_splice_channel
                        elif type == "Regional" or type == "National":
                            Cost_nonsplice_channel = (int(E_value)*1.25) * int(rotates) * (int(spot_duration) /10)
                            print "Computed cost of the National and regional channels", Cost_nonsplice_channel
logger = logging.getLogger('test_all_combs')
logger.setLevel(logging.INFO)


if not logger.handlers:
    # create a file handler
    handler = logging.FileHandler('/home/admin/pycharm/pycharmprojects/LOGS/logger.log')
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

#path = "/home/kiran/DSP_MixAlgs/mix-algs/media_packages/"
path = "/home/admin/pycharm/MixAlgos/mix-algs/media_packages/"

for cnt in range(0, len(regions)-1):
    #regions_str, = (regions for regions in regions)
    age_str = '\"' + ages[random.randint(0, len(ages)-1)] + '\"'
    gender_str = '\"' + genders[random.randint(0, len(genders)-1)] + '\"'
    cat_str = '\"' + product_sub_cats[random.randint(0, len(product_sub_cats)-1)] + '\"'
    profile_str = '\"' + profiles[random.randint(0, len(profiles)-1)] + '\"'
    profile_str = profile_str.replace('MF', '')
    profile_str = profile_str.replace('M', '')
    profile_str = profile_str.replace('F', '')

    command_str = "python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16" + " -a " + age_str + " -g " + gender_str + \
                  " -r " + region_m + " -c " + cat_str + " -m " + profile_str + " -p " + \
                  str(random.randint(0, 20)) + " -s " + str(spot_duration[random.randint(0, 2)]) + " -b " + \
                  str(random.randint(0, 50000))

    logger.info(command_str)
    start_time = time.time()
    os.system(command_str)
    logger.info('Time taken' + str(time.time() - start_time))
   # print 'Time taken' + str(time.time() - start_time)
"""
