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
print "Tax,Gender,Budget_Shoot,Budget_diff_percentage,Result_Actl_Cost,Actl_Cost_Mongo,Actl_Cost_Response,Result_Cost,Result_Discount,Result_Cutoff,Input_command"
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
    print input_command,',',
#    command_str = "python /home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/media_packages/compute_media_packages_v3.py -f $HOME -d 21-10-16 -a 15+ -g 'Female' -r 'Bihar, Kerala, Jharkhand, Orissa' -c 'Hair Care' -m 'Early Professionals' -p 7 -s 25 -b 411920"
#    print command_str
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
 # Tax is 15% of discounted_package_cost
    def tax_calc():
        dis_pkg_cost = data['package']['discounted_package_cost']
        tax = (15 * int(dis_pkg_cost)) / 100
        #print tax
        tax_out = data['package']['tax_amount']
        #print tax_out
        if round(tax) == tax_out or round(tax) == (tax_out + 1) or round(tax) == (tax_out - 1) :
            return True
        else:
            return False

    # Validating gender (input & response)
    def gender_check():
        gender_out = data['package']['gender']
        #print gender_out
	k = "Kids"
	a = "All Adults"
        gender_in,category_in,profile_in,budget_in = inputs_from_cmd()
        #print gender_in
        if str(gender_in) == '\"'+gender_out+'\"':
            return True
        elif (str(gender_in) != '\"'+gender_out+'\"') and (str(profile_in) == "Kids" or str(profile_in) == "All Adults"):
            return True
        else:
            return False
    # Budget over shoot and under shoot calc
    def budget_shoot():
        #Taking budget input from inuts_from_cmd function
        gender_in, category_in, profile_in, budget_in = inputs_from_cmd()
        package_cost = data['package']['package_cost']
        budget_diff = int(package_cost) - int(budget_in)
	#print budget_in, package_cost, budget_diff
        if budget_diff >= 0:
            bud_diff_percent = round(((abs(budget_diff)*100)/int(budget_in)),2)
            if bud_diff_percent > 5:
                return 'Overshoot', bud_diff_percent
            else:
                return 'No_Overshoot', bud_diff_percent
        elif budget_diff < 0:
            bud_diff_percent = round(((abs(budget_diff) * 100) / int(budget_in)), 2)
            if bud_diff_percent > 5:
                return 'Undershoot', bud_diff_percent
            else:
                return 'No_undershoot', bud_diff_percent
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

    def actual_cost_check():
        for i in range(0,len(data['package']['region'])):
            if data['package']['region'][i]['channel_order'] == []:
                continue
                #If channel_order is not empty, then compute the actual cost
            else:
                region_name = data['package']['region'][i]['region_name']
                for j in range(0,len(data['package']['region'][i]['channels'])):
                    channel_name = data['package']['region'][i]['channels'][j]['channel_name']
                    type_out = data['package']['region'][i]['channels'][j]['type']
                    actual_cost_out = data['package']['region'][i]['channels'][j]['actual_cost']
                    rotates_out = data['package']['region'][i]['channels'][j]['rotates']
                    cost_out = data['package']['region'][i]['channels'][j]['cost']
                    #print channel_name,',',type,',',actual_cost_out,',',rotates_out,',',cost_out
                    E_value = er_from_mongo(region_name,channel_name)
		    if E_value == '' or E_value == [] or E_value == None:
			continue
		    else:
                    	spot_dur =  data['package']['spot_duration']
                    	#actual cost computation
                    	actual_cost_computed = int(E_value) * (int(spot_dur) / 10)
                    	if type_out == 'Spliced':
                    	    if round(actual_cost_computed) == actual_cost_out:
			    	return 'Pass',actual_cost_computed,actual_cost_out
                            else:
                       	    	return 'Fail',actual_cost_computed,actual_cost_out
                    	elif type_out == 'National' or type_out == 'Regional':
                            if actual_cost_out >= (actual_cost_computed * 0.96) and actual_cost_out <= (actual_cost_computed * 1.25):
                                return 'Pass',actual_cost_computed,actual_cost_out
                            else:
                                return 'Fail',actual_cost_computed,actual_cost_out
    def cost_check():
	for i in range(0,len(data['package']['region'])):
            if data['package']['region'][i]['channel_order'] == []:
                continue
                #If channel_order is not empty, then compute the actual cost
            else:
                region_name = data['package']['region'][i]['region_name']
                for j in range(0,len(data['package']['region'][i]['channels'])):
		    actual_cost_out = data['package']['region'][i]['channels'][j]['actual_cost']
		    rotates_out = data['package']['region'][i]['channels'][j]['rotates']
		    cost_out = data['package']['region'][i]['channels'][j]['cost']
		    cost_computed = int(actual_cost_out) * int(rotates_out)
		    if cost_computed == cost_out or cost_out <= (cost_computed - 1) or cost_out >=  (cost_computed + 1):
			return True
		    else:
			return False   

    def discounted_package_cost():
	sum_o = 0
	for i in range(0,len(data['package']['region'])):
            if data['package']['region'][i]['channel_order'] == []:
                continue
                #If channel_order is not empty, then compute the actual cost
            else:
		dis_reg_cost = data['package']['region'][i]['discounted_region_cost']
		sum_o += dis_reg_cost
	    discounted_package_cost_out = data['package']['discounted_package_cost']
	    if discounted_package_cost_out == sum_o:
		return True
	    else:
		return False
		
    #Discount should not be more than 10%
    def discount():
        pack_cost = data['package']['package_cost']
        #print pack_cost
        disc_pack_cost = data['package']['discounted_package_cost']
        #print disc_pack_cost
        discount = pack_cost - disc_pack_cost
        #print discount
        #discount % w.r.t pack_cost
        disc_percentage = (discount * 100) / pack_cost
        #print disc_percentage
        if round(disc_percentage) <= 10:
            return True
        else:
            return False 

    def cutoff_from_mongo(region_name, channel_name):
        # cutoff_rate from mongo
        mongo_entire = db.effective_rates.find({})
        for rates in mongo_entire:
            # print rates
            Erate = (rates['region'] + ',', rates['channel'] + ',', rates['cutoff_rate'])
            region_m = Erate[0][:-1]
            channel_m = Erate[1][:-1]
            if region_name == region_m and channel_name == channel_m:
                return Erate[2]


    def cutoff_rate_check():
        final_cost_compute = 0
        # cutoff_rate from mongo
        for i in range(0, len(data['package']['region'])):
            #print 'i',i
            if data['package']['region'][i]['channel_order'] == []:
                continue
                # If channel_order is not empty, then compute the actual cost
            else:
                sum_c = 0
                for j in range(0, len(data['package']['region'][i]['channels'])):
                    #print 'j',j
                    channel_name = data['package']['region'][i]['channels'][j]['channel_name']
                    type_out = data['package']['region'][i]['channels'][j]['type']
                    region_name = data['package']['region'][i]['region_name']
                    if region_name == 'National' and (type_out == 'National' or type_out == 'Regional'):
                        region_name = data['package']['region'][i]['region_name']
                    elif region_name == 'National' and type_out == 'Spliced':
                        region_name = 'DTH'
                    else:
                        region_name = data['package']['region'][i]['region_name']
                    E_value = cutoff_from_mongo(region_name, channel_name)
                    #print E_value
                    spot_duration = data['package']['spot_duration']
                    actual_compute = E_value * (spot_duration / 10)
                    rotates_out = data['package']['region'][i]['channels'][j]['rotates']
                    cost_compute = actual_compute * rotates_out
                    #print 'region_name', region_name, 'channel_name', channel_name, 'type', type_out, 'E_value', E_value, 'actual_compute', actual_compute, 'rotates', rotates_out, 'cost_compute', cost_compute
                    sum_c += cost_compute
                    #print 'sum_c', sum_c
            final_cost_compute += sum_c
            #print 'final', final_cost_compute
        #print 'minimum_package_cost', data['package']['minimum_discounted_cost']
        min_pakg_cost = data['package']['minimum_discounted_cost']
        final  = round(final_cost_compute)
        #print 'Min_package_cost',',',min_pakg_cost,',','Final_computed',',',final,',',
        if final == min_pakg_cost or min_pakg_cost <= (final - 1) or min_pakg_cost >= (final + 1)  :
            return True
        else:
            return False


# Calculation of package_cost by adding all the discounted_region_cost
    def package_cost_calc():
        sum = 0
        for region in data['package']['region']:
            disc_reg_cost = []
            disc_reg_cost = int(region.get('discounted_region_cost'))
            #print disc_reg_cost
            sum = sum + disc_reg_cost
        #print sum
        #comparing all the sum of discounted_region_cost with package_cost of response
        package_cost_out = data['package']['package_cost']
        #print package_cost_out
        if package_cost_out == sum or package_cost_out == (sum + 1) or package_cost_out == (sum - 1):
            return True
        else:
            return False

#############################
##Calling the functions
    #Tax check
    tax = tax_calc()
    if tax == True:
	print 'Pass',',',
    else:
        print 'Fail',',',
    #Gender check
    gen = gender_check()
    if gen == True:
        print 'Pass',',',
    elif gen == False:
        print 'Fail',',',
    #Budget shoot
    budget_shoot,bud_diff_percentage = budget_shoot()
    print budget_shoot,',',bud_diff_percentage,',',
    #Actual_cost
    result,actual_cost_comp,actual_cost_response = actual_cost_check()
    print result,',',actual_cost_comp,',',actual_cost_response,',',
    #Cost check
    cost = cost_check()
    if cost == True:
	print 'Pass',',',
    else:
	print 'Fail',',',
    #Discount
    discount_o = discount()
    if discount_o == True:
	print 'Pass',',',
    else:
	print 'Fail',',',
    #Cutoff
    cut_off = cutoff_rate_check()
    if cut_off == True:
        print "Pass",',',
    else:
        print "False",',',
    print input_command
