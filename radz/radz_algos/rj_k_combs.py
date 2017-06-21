from pymongo import MongoClient
import toml
import logging
import random
import os
import time
import commands

with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())

mongo_client = MongoClient(config["app"]["mongo_conn_str"])

# Connect to DB
db = mongo_client.dsp

# get all regions
regions = list(db.regions.distinct("region"))
genders = ['Male', 'Female', 'Male,Female']
#spot_duration = [10, 20, 30]
spot_duration = [15,25]
ages = ["30+", "22+", "15-21", "22-30", "50+", "22-40", "09-21", "04-14", "15+"]

#profiles = list(db.profile_to_tg.distinct("audience_type"))
#product_sub_cats = db.profile_to_brand.distinct('category')

logger = logging.getLogger('test_all_combs')
logger.setLevel(logging.INFO)

if not logger.handlers:
    # create a file handler
    handler = logging.FileHandler('/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/test_inputs/test_all_combs.log')
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

path = "media_packages/"
print "Status,Time(s),Input"
for cnt in range(0, 1000):

    reg_iter = random.sample(range(0, len(regions)-1), random.randint(1, len(regions)-1))
    current_regions = []
    for i in reg_iter:
        current_regions.append(regions[i])
    current_regions_str = '\"' + ','.join(current_regions) + '\"'

    age_str = '\"' + ages[random.randint(0, len(ages)-1)] + '\"'
    gender_str = '\"' + genders[random.randint(0, len(genders)-1)] + '\"'
    cat_prof = random.choice(list(open('cat_prof_map.txt'))).rstrip()
    command_str = "python " + path + "compute_media_packages_v3.py -f $HOME -d 21-10-16" + " -a " + age_str + " -g " + gender_str + \
                  " -r " + current_regions_str  +  cat_prof + " -p " + \
                  str(random.randint(5, 30)) + " -s " + str(spot_duration[random.randint(0, 1)]) + " -b " + \
                  str(random.randint(0, 3000000))
    input_command = command_str.replace(',',' ')	
    #print input_command +',',
    logger.info(command_str)
    start_time = time.time()
    try:
        status, output = commands.getstatusoutput(command_str)
	print str(status) +',',
    except ValueError:
	print "wrong input," 
	continue
   # os.system(command_str)
    logger.info('Time taken' + str(time.time() - start_time))
    time_taken = str(time.time() - start_time)
    print str(time_taken) +',',
    print input_command
