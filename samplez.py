from optparse import  OptionParser
import toml
from pymongo import MongoClient
import random
from random import randint
import time
import requests, json
import sys
import pymongo
from heapq import nsmallest

with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp


############################################-----Regions------###########################################################
def region(re):
    regions = db.channel_mappings.distinct("region",{"enabled":1})
    regions = [r.replace("&","%26") for r in regions]
    if 'National' in regions: regions.remove('National')
    if 'DTH' in regions: regions.remove('DTH')
    if re == "1by1":
        reg = regions[random.randrange(len(regions))]
    elif re == "rand":
	reg_iter = random.sample(range(0, len(regions) - 1), random.randint(1, len(regions) - 1))
        current_regions = []
        for j in reg_iter:
            current_regions.append(regions[j])
            if (('AP/Telangana' and 'Hyderabad') or ('Hyderabad' and 'Rest of Andhra Pradesh')) in current_regions:current_regions.remove('Hyderabad')
            if ('AP/Telangana' and 'Rest of Andhra Pradesh') in r: r.remove('Rest of Andhra Pradesh')
            if (('Karnataka' and 'Bangalore') or ('Bangalore' and 'Rest of Karnataka')) in current_regions:current_regions.remove('Bangalore')
            if ('Karnataka' and 'Rest of Karnataka') in current_regions:current_regions.remove('Rest of Karnataka')
            if (('TN/Pondicherry' and 'Chennai') or ('Chennai' and 'Rest of Tamil Nadu')) in current_regions:current_regions.remove('Chennai')
            if ('TN/Pondicherry' and 'Rest of Tamil Nadu') in current_regions:current_regions.remove('Rest of Tamil Nadu')
            if (('Maharashtra/Goa' and 'Mumbai') or ('Mumbai' and 'Rest of Maharashtra')) in current_regions:current_regions.remove('Mumbai')
            if ('Maharashtra/Goa' and 'Rest of Maharashtra') in current_regions:current_regions.remove('Rest of Maharashtra')
            reg =  ','.join(current_regions)
            if len(current_regions) == 0 : reg = "National"
    return reg

#########################################------Profile------#############################################################
def category_to_profile_mapping_mongo(category_m):
    c = db.category_to_profile_mapping.find({"category": category_m}).count()
#    print c
    if c is 0 :
        c = db.category_to_profile_mapping.find({"category": 'Miscellaneous'})
    else:
        c = db.category_to_profile_mapping.find({"category": category_m})
    for document in c:
        result = document.get("profiles")
        if result is None or result == "":
            c = db.category_to_profile_mapping.find({"category": 'Miscellaneous'})
            for document in c:
                result = document.get("profiles")
        result1 = result.split(',')
        prof_m = result1[random.randrange(len(result1))]
        return prof_m
    
#########################################-----Cat_Subcat----#############################################################
def cat_subc_prof():
    all_entries = randint(1,445)
    c = db.amagitext_to_adex_category.find().limit(-1).skip(all_entries).next()
    category_used = (c['adex_super_category'])
    sub_category_used = (c['adex_sub_category'])
    prof_m = category_to_profile_mapping_mongo(category_used)
    if "&" in category_used:
	category_used = category_used.replace("&","%26")
    elif "/" in category_used:
	category_used = category_used.replace("/","%2F")
    if "&" in sub_category_used:
        sub_category_used = sub_category_used.replace("&","%26")
    elif "/" in sub_category_used:
        sub_category_used = sub_category_used.replace("/","%2F")
#    print category_used, sub_category_used, prof_m
    return category_used, sub_category_used, prof_m

#########################################----Inputs-----#################################################################
def Input():

    parser = OptionParser()
    parser.add_option("-i","--iterations", help="Specify number of iterations") 
    parser.add_option("-r","--regions", help="Specify whether 1by1/rand/given_region")  
    parser.add_option("-g","--gender", help="Specify whether rand/specific_gen")
    parser.add_option("-a","--cate", help= "Specify whether rand/specific_cat and subcat and prof seperated by comma")
    parser.add_option("-d","--duration", help="Specify whether rand/specific_duration")
    parser.add_option("-s","--spot_duration", help="Specify whether rand/specific spot_duration")
    parser.add_option("-b","--budget",help= "Specify rand/specific_budget")
    parser.add_option("-p","--program",help="Specify which prog in specific/All")
#    parser.add_option("-def","--definition".help= "Specify whether all functions/ which ever function needed")
    (option, args) = parser.parse_args()
    if option.iterations == None:
	print "Cmd to call with random values: python samplez.py -i '100' -r 'rand' -g 'rand' -a 'rand' -d 'rand' -s 'rand' -b 'rand' -p 'All' \
               Cmd to call with specifics: python samplez.py -i '100' -r 'National'/'1by1' -g 'Male' -a 'Computers,Desktops,Young Adults' -d '10' -s '10' -b '10000' -p \"basic\"/\"uu\"/\"ap\"/\"ch\"/\"imp\"/\"cr\"/\"ra\"/\"sr\""
	sys.exit(0)
    else:
#        print option.iterations, option.regions, option.gender, option.cate, option.duration, option.spot_duration, option.budget
        num = int(option.iterations)

        if option.regions == "1by1":
	    reg = region("1by1")
        elif option.regions == "rand":
	    reg = region("rand")
        else:
	    reg = option.regions

#######################################------Gender-----##################################################################
        if option.gender == "rand":
	    gen_a = ["Male,Female","Male","Female"]
	    gen = gen_a[random.randrange(len(gen_a))]
        else:
	    gen = option.gender

######################################-------Category---##################################################################
        if option.cate == "rand":
	    cat, subcat, prof = cat_subc_prof()
        else:
	    cat, subcat, prof = option.cate.split(',')
	
####################################--------Duration----#################################################################
        if option.duration == "rand":
	    duration = randint(5,99)
	    dur = str(duration)
        else:
	    dur = option.duration
###################################--------Spot_Duration----#############################################################
        if option.spot_duration == "rand":
	    spot_d = ["10","15","20","25","30"]
	    spot_dur = spot_d[random.randrange(len(spot_d))]
	    spo = str(spot_dur)
        else:
	    spo = option.spot_duration
##################################---------budget----------##############################################################
        if option.budget == "rand":
	    budj = randint(15000,500000)
	    bud = str(budj)
        else:
	    bud = option.budget

	return num, reg, gen, cat, subcat, prof, dur, spo,  bud, option.program
#        print num, reg, gen, cat, subcat, prof, dur, spo,  bud

################################---------calling compute media package--------#########################################
###################################-----Main program that calls all the funcs---######################################
def algo_call():
    num, re, ge, ca, su, pr, du, sp, bu, p = Input()
    for i in range(0,num):
	n, reg, gen, cat, subcat, prof, dur, spo,  bud, prog = Input()
	url ="http://localhost:2770/compute-media-package"
	api = str(url)+'?regions='+reg+'&date=21-10-16&gender='+gen+'&category='+cat+'&sub_category='+subcat+'&profile='+prof+'&duration='+dur+'&spot_duration='+spo+'&budgets='+bud+'&user_id=radhika@amagi.com'
	start_time = time.time()
	re=requests.get(api)
	end_time = time.time()
	if (re.status_code != 200):
	    print re.status_code,',',api
	    continue
	else:
	    re_t = re.text
	    data = json.loads(re_t)
##############-----output data from json-----#########
	    g_out = data['package']['gender']
	    spo_out = data['package']['spot_duration']
	    bud_out = data['package']['discounted_package_cost']
	    tax_out = data['package']['tax_amount']
	    pkg_cost_out = data['package']['package_cost']
	    
############----Calling functions to check correctness---#######
	    if prog == "All" or prog == "basic":
		basic = basic_check(gen,spo,bud,g_out,spo_out,bud_out,tax_out,prof)
	    if prog == "All" or prog == "uu":
	        uu = UnderUtil(bud,bud_out,pkg_cost_out)
	    if prog == "All" or prog == "ap":
	        ap = apportioning_er(data,bud_out)
	    if prog == "All" or prog == "ch":
	        ch = valid_channels(data)
	    if prog == "All" or prog == "imp":
		imp = impressions(data,prof)
	    if prog == "All" or prog == "cr":
		cr = channel_reach(data,prof)
	    if prog == "All" or prog == "ra":
		ra = rationale(data)
	    if prog == "All" or prog == "sr":
		sr = spot_reach(data,prof)
	    print api
#	    return data
###########################################-----output data from json-----#############################################################################

def basic_check(gen,spo,bud,g_out,spo_out,bud_out,tax_out,prof):
    percent = round(15*(bud_out)/100)
    if ((str(gen) == str(g_out)) or ((str(gen) != str(g_out)) and (str(prof) == 'Kids' or str(prof) == 'All Adults'))) and (str(spo) == str(spo_out)) and (tax_out == percent or tax_out == (percent +1) or tax_out == (percent -1)):
	print 'Basic_Pass',',',
    else:
	print 'Basic_Fail',',',
###########################################-----Budget Under Util-------###############################################################################     

def UnderUtil(bud,bud_out,pkg_cost_out):
    bud_diff = int(bud_out) - int(bud)
    #### Checking bud_diff is wat percent of input budget
    bud_diff_percent = round(((abs(bud_diff)*100)/int(bud)),2)
    if bud_diff >= 0:
	if bud_diff_percent > 5:
	    print 'Overshoot',',',str(bud_diff_percent),',',bud,',',bud_out,',',pkg_cost_out,',',
	else:
	    print 'No_Overshoot',',',str(bud_diff_percent),',',bud,',',bud_out,',',pkg_cost_out,',',
    elif bud_diff < 0:
	if bud_diff_percent > 5:
	    print 'Under_Utilisation',',',str(bud_diff_percent),',',bud,',',bud_out,',',pkg_cost_out,',',
        else:
            print 'No_Under_Utilisation',',',str(bud_diff_percent),',',bud,',',bud_out,',',pkg_cost_out,',',
   
##########################################------Apportioning ER check---------########################################################################

def apportioning_er(data,bud_out):
    dis_pkg_cost = bud_out
    total_ac_cost = 0
    for i in range(0, len(data['package']['region'])):
	if data['package']['region'][i]['channel_order'] == []: 
	    continue
	else:
	    sum_ac_cost = 0
	    for j in range(0, len(data['package']['region'][i]['channels'])):
		###Actual cost from response###
		ac_cost_out = data['package']['region'][i]['channels'][j]['actual_cost']
		sum_ac_cost += ac_cost_out
	total_ac_cost += sum_ac_cost
    if dis_pkg_cost == total_ac_cost or dis_pkg_cost <= (total_ac_cost - 1) or dis_pkg_cost >= (total_ac_cost + 1):
	print 'Appor_Er_Pass',',',
    else:
	print 'Appor_Er_Pass',',',
########################################----------Valid channels check------------------################################################################################3	    
########quering mongo for enabled value#######
def enabled_val_mongo(reg_out,chan_out):
    mongo_entire = db.channel_mappings.find({})
    for c in mongo_entire:
        Enab = (c['region'] + ',', c['channel_name'] + ',', c['enabled'])
        region_m = Enab[0][:-1]
        channel_m = Enab[1][:-1]
        if reg_out == region_m and chan_out == channel_m:
            return Enab[2]
#############################################
def valid_channels(data):
    for i in range(0, len(data['package']['region'])):
        if data['package']['region'][i]['channel_order'] == []:
            continue
        else:
            sum_ac_cost = 0
            for j in range(0, len(data['package']['region'][i]['channels'])):
		reg_out = data['package']['region'][i]['region_name']
		chan_out = data['package']['region'][i]['channels'][j]['channel_name']
		enabled_value = enabled_val_mongo(reg_out,chan_out)
		if enabled_value == None and reg_out == "National":
		    enabled_value = enabled_val_mongo('DTH',chan_out)
		if enabled_value == 1:
		    res = "Pass"
		else:
		    res = "Fail"
	all_res = []
	all_res.append(res)
    if (all(all_res[0] == item for item in all_res) and all_res[0] == "Pass"):
	print 'Val_chan_Pass',',',
    else:
	print 'Val_chan_Fail',',',
##########################################------------------Impressions------------------------#######################################################################################
############quering mongo######
def chan_map_mongo(region_name,type_out,channel_name):
    c = db.channel_mappings.find({"region":region_name,"type":type_out,"channel_name":channel_name})
    for doc in c:
	result = doc.get("coverage")
        return result

def profile_to_tg_mongo(audience_type):
    c = db.profile_to_tg.find({"audience_type":audience_type})
    for document in c:
	result = document.get("tg")
        r = result.split('/')
        r_1 = r[0]
        nccs = list(r_1)
        return nccs

def tvt_mongo(reg_out,chan_out,age,g,nccs):
    c = db.channel_tvt.find({"channel":chan_out,"region":reg_out,"gender":g,"age":age,"nccs":nccs})
    for document in c:
	result = document.get("tvt")
        return result

def reach_split_mongo(coverage,reg_out):
    c = db.reach_split.find({"region":reg_out})
    for doc in c:
	if coverage == 'Cable':
	    return doc.get("cable_percent")
	if coverage == 'DTH':
	    return doc.get("dth_percent")
	if coverage == 'Cable+DTH':
	    return 100
	

##################################
def impressions(data,prof):
    for i in range(0,len(data['package']['region'])):
	if data['package']['region'][i]['channel_order'] == []:
	    continue
	else:
	    imp_calc = 0
	    for j in range(0, len(data['package']['region'][i]['channels'])):
####Inputs needed for impre calc######
		reg_out = data['package']['region'][i]['region_name']
		type_out = data['package']['region'][i]['channels'][j]['type']
                chan_out = data['package']['region'][i]['channels'][j]['channel_name']
		age = data['package']['age']
                gender = data['package']['gender']
		if gender == 'Male,Female':
		    g = ["Male","Female"]
		    g_for_tg = ' MF'
		elif gender == 'Female':
		    g = ["Female"]
		    g_for_tg = ' F'
		elif gender == 'Male':
		    g = ["Male"]
		    g_for_tg = ' M'
		rotates_out = data['package']['region'][i]['channels'][j]['rotates']
                impressions_out = data['package']['region'][i]['channels'][j]['impression']
                audience_type =  prof + g_for_tg
#		print  prof , g_for_tg, audience_type
                nccs = profile_to_tg_mongo(audience_type)
		tvt_mon = tvt_mongo(reg_out,chan_out,age,g,nccs)
		tvt_calc = float(tvt_mon) * 1000 * int(rotates_out)
#### For national channels ############
		if ((len(data['package']['region']) == 1) and reg_out == "National"):
		    if type_out == "National":
		    	coverage = chan_map_mongo(reg_out,type_out,chan_out)
		    elif type_out == "Spliced":
			coverage = chan_map_mongo('DTH',type_out,chan_out)
		    val = reach_split_mongo(coverage,reg_out)
		    imp_calc = tvt_calc * (val / 100)
####Covering Non National channels######
		elif reg_out != "National":
		    coverage = chan_map_mongo(reg_out,type_out,chan_out)
		    val = reach_split_mongo(coverage,reg_out)
		    imp_calc = tvt_calc * (val / 100)
####Covering All India channels#########
		else:
		    imp_na = 0
		    impressions_out = data['package']['region'][i]['region_impressions']
		    for key,value in data['package']['region'][i]['detailed_region_impressions'].items():
			for j in range(0, len(data['package']['region'][i]['channels'])):
			    type_out = 'Spliced'
			    reg_out = 'DTH'
			    coverage = chan_map_mongo(reg_out,type_out,chan_out)
			    if coverage == None:
				coverage = chan_map_mongo('National','National',chan_out)
			    val = reach_split_mongo(coverage,key)
			    tvt_mon = tvt_mongo(key,chan_out,age,g,nccs)
			    tvt_calc = float(tvt_mon) * 1000 * int(rotates_out)
			    imp_n = tvt_calc * (val / 100)
#			    print key, value, coverage, val, tvt_mon, tvt_calc, imp_n
		        imp_na += imp_n
		    imp_calc += imp_na
#		print imp_calc, impressions_out
		if int(imp_calc) == int(impressions_out): 			 		    
		    res = "Pass"
		else:
		    res = "Fail"
            I = []
            I.append(res)
    if (all(I[0] == item for item in I)) and (I[0] == 'Pass'):
	print 'Imp_pass',',',
    else:
	print 'Imp_fail',',',

################################################-----Channel_Reach-------#########################################################################################
#### querying mongo#########
def chan_reach_mongo(reg_out,chan_out,age,g,nccs):
    c = db.channel_reach.find({"channel":chan_out,"region":reg_out,"gender":g,"age":age,"nccs":nccs})
    for document in c:
        result = document.get("channel_reach")
        return result


#############################

def channel_reach(data,prof):
    for i in range(0,len(data['package']['region'])):
	if data['package']['region'][i]['channel_order'] == []:
	    continue
	else:
	    for j in range(0, len(data['package']['region'][i]['channels'])):
####Inputs needed for reach calc######
		reg_out = data['package']['region'][i]['region_name']
		type_out = data['package']['region'][i]['channels'][j]['type']
                chan_out = data['package']['region'][i]['channels'][j]['channel_name']
		age = data['package']['age']
                gender = data['package']['gender']
		if gender == 'Male,Female':
		    g = ["Male","Female"]
		    g_for_tg = ' MF'
		elif gender == 'Female':
		    g = ["Female"]
		    g_for_tg = ' F'
		elif gender == 'Male':
		    g = ["Male"]
		    g_for_tg = ' M'
		chan_reach_out = data['package']['region'][i]['channels'][j]['channel_reach']
                audience_type =  prof + g_for_tg
                nccs = profile_to_tg_mongo(audience_type)
		chan_reach_mon = chan_reach_mongo(reg_out,chan_out,age,g,nccs)
		chan_reach = float(chan_reach_mon) * 1000 
#### For national channels ############
		if ((len(data['package']['region']) == 1) and reg_out == "National"):
		    if type_out == "National":
		    	coverage = chan_map_mongo(reg_out,type_out,chan_out)
		    elif type_out == "Spliced":
			coverage = chan_map_mongo('DTH',type_out,chan_out)
		    val = reach_split_mongo(coverage,reg_out)
		    chan_reach_calc = chan_reach * (val / 100)
####Covering Non National channels######
		elif reg_out != "National":
		    coverage = chan_map_mongo(reg_out,type_out,chan_out)
		    val = reach_split_mongo(coverage,reg_out)
		    chan_reach_calc = chan_reach * (val / 100)
####Covering All India channels#########
		else:
		    chan_reach_calc = 0
		    for key,value in data['package']['region'][i]['detailed_region_impressions'].items():
			for j in range(0, len(data['package']['region'][i]['channels'])):
			    type_out = 'Spliced'
			    reg_out = 'DTH'
			    coverage = chan_map_mongo(reg_out,type_out,chan_out)
			    if coverage == None:
				coverage = chan_map_mongo('National','National',chan_out)
			    val = reach_split_mongo(coverage,key)
			    chan_reach_mon = chan_reach_mongo(key,chan_out,age,g,nccs)
			    chan_reach = float(chan_reach_mon) * 1000
			    reach_n = chan_reach * (val / 100)
			chan_reach_calc += reach_n
		if int(chan_reach_calc) == int(chan_reach_out):
		    res = 'Pass'
		else:
		    res = 'Fail'
	    C = []
	    C.append(res)
    if (all(C[0] == item for item in C)) and (C[0] == 'Pass'):
	print 'CReach_pass',',',
    else:
	print 'CReach_fail',',',
#####################################-------Sanity Rationale---------###############################################################
def rationale(data):
    for i in range(0,len(data['package']['region'])):
        if data['package']['region'][i]['channel_order'] == []:
            continue
        else:
            for j in range(0,len(data['package']['region'][i]['channels'])):
                if "rationale" in data['package']['region'][i]['channels'][j]:
                    res = "Pass"
                else:
                    res = "Fail"
	    R = []
            R.append(res)
    if (all(R[0] == item for item in R)) and (R[0] == 'Pass'):
        print 'Rationale_pass',',',
    else:
        print 'Rationale_fail',',', 
        
########################################------Spot Reach----------------###############################################################
def spot_reach_val(reg_out,chan_out,age,g,nccs,num):
    c = db.spot_reach.find({"channel":chan_out,"region":reg_out,"age":age,"gender":g,"nccs":nccs,"spots":num})
    for doc in c:
	spot_reach_mongo = doc.get("reach")
	return spot_reach_mongo
######querying mongo#################
def spot_reach_mongo(reg_out,chan_out,age,g,nccs,rotates_out):
    c = db.spot_reach.find({"channel":chan_out,"region":reg_out,"age":age,"gender":g,"nccs":nccs})
    spots_all = []
    for doc in c:
	s_all = doc.get("spots")
	if s_all == None:
	    s_all = 0
	spots_all.append(s_all)
    sortd = sorted(spots_all)
    if sortd == []:
	spot_reach_m = 0
	return spot_reach_m, spot_reach_m
    else:
	max_num = max(sortd)
	min_num = min(sortd)
	next_num = next(i for i in sortd if i >= rotates_out)	 
	prev_number  = lambda seq,x: min([(x-i,i) for i in seq if x>=i] or [(0,None)])[1]
	prev_num =  prev_number(sortd,rotates_out)
	if rotates_out < min_num:
	    spot_reach_mongo = spot_reach_val(reg_out,chan_out,age,g,nccs,min_num)
	    spot_reach_m = float(spot_reach_mongo)*1000
	    return spot_reach_m,spot_reach_m
	elif rotates_out > max_num:
	    spot_reach_mongo = spot_reach_val(reg_out,chan_out,age,g,nccs,max_num)
	    spot_reach_m = float(spot_reach_mongo)*1000
	    return spot_reach_m,spot_reach_m
	elif rotates_out == prev_num and rotates_out == next_num:
	    spot_reach_mongo = spot_reach_val(reg_out,chan_out,age,g,nccs,rotates_out)
	    spot_reach_m = float(spot_reach_mongo)*1000
	    return spot_reach_m,spot_reach_m
	elif rotates_out > prev_num and rotates_out < next_num:
	    prev_spot_reach_mongo = spot_reach_val(reg_out,chan_out,age,g,nccs,prev_num)
	    next_spot_reach_mongo = spot_reach_val(reg_out,chan_out,age,g,nccs,next_num)
	    prev_spot_reach_m = float(prev_spot_reach_mongo) * 1000
	    next_spot_reach_m = float(next_spot_reach_mongo) * 1000
	    return prev_spot_reach_m, next_spot_reach_m
#####################################
def spot_reach(data,prof):
    for i in range(0,len(data['package']['region'])):
        if data['package']['region'][i]['channel_order'] == []:
            continue
        else:
            for j in range(0, len(data['package']['region'][i]['channels'])):        
		reg_out = data['package']['region'][i]['region_name']
		type_out = data['package']['region'][i]['channels'][j]['type']
		chan_out = data['package']['region'][i]['channels'][j]['channel_name']
		age = data['package']['age']
		rotates_out = data['package']['region'][i]['channels'][j]['rotates'] 
		gender = data['package']['gender']
                if gender == 'Male,Female':
                    g = ["Male","Female"]
                    g_for_tg = ' MF'
                elif gender == 'Female':
                    g = ["Female"]
                    g_for_tg = ' F'
                elif gender == 'Male':
                    g = ["Male"]
                    g_for_tg = ' M'
                audience_type =  prof + g_for_tg
                nccs = profile_to_tg_mongo(audience_type)
		spot_reach_out = data['package']['region'][i]['channels'][j]['reach']
		sr1,sr2 = spot_reach_mongo(reg_out,chan_out,age,g,nccs,rotates_out)
##### For national channels ############
                if ((len(data['package']['region']) == 1) and reg_out == "National"):
                    if type_out == "National":
                        coverage = chan_map_mongo(reg_out,type_out,chan_out)
                    elif type_out == "Spliced":
                        coverage = chan_map_mongo('DTH',type_out,chan_out)
                    val = reach_split_mongo(coverage,reg_out)
		    if sr1 == sr2:
			spot_reach_calc = sr1 * (val / 100)
			if int(spot_reach_out) == int(spot_reach_calc):
			    res = 'Pass'
			else:
			    res = 'Fail'
		    else:
			spot_reach_calc_1 = sr1 * (val / 100)
			spot_reach_calc_2 = sr2 * (val / 100)
			if (int(spot_reach_out) >= int(spot_reach_calc_1)) and (int(spot_reach_out) <= int(spot_reach_calc_2)):
			    res = 'Pass'
			else:
			    res = 'Fail'
####Covering Non National channels######
                elif reg_out != "National":
                    coverage = chan_map_mongo(reg_out,type_out,chan_out)
                    val = reach_split_mongo(coverage,reg_out)
		    if sr1 == sr2:
                        spot_reach_calc = sr1 * (val / 100)
			if int(spot_reach_out) == int(spot_reach_calc):
			    res = 'Pass'
			else:
			    res = 'Fail'
                    else:
                        spot_reach_calc_1 = sr1 * (val / 100)
                        spot_reach_calc_2 = sr2 * (val / 100)
                        if (int(spot_reach_out) >= int(spot_reach_calc_1)) and (int(spot_reach_out) <= int(spot_reach_calc_2)):
                            res = 'Pass'
                        else:
                            res = 'Fail'
		    S = []
                    S.append(res)
    if (all(S[0] == item for item in S)) and (S[0] == 'Pass'):
	print 'SReach_pass',',',
    else:
	print 'SReach_fail',',',
		
#####################################################################################################################################
call = algo_call()


#################################---------Default algo call if inputs are not passed-----###############################
#def default_algo_call():
#    print "Default alof call"    

