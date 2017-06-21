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
import logging

logger = logging.getLogger('rj_samplez')
logger.setLevel(logging.INFO)

if not logger.handlers:
    # create a file handler
    handler = logging.FileHandler('hello.log')
    handler.setLevel(logging.DEBUG)
    # add the handlers to the logger
    logger.addHandler(handler)

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
	    spot_d = ["10","15","20","25","30","35","40"]
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
#        print num, reg, gen, cat, subcat, prof, dur, spo,  bud, option.program

################################---------calling compute media package--------#########################################
###################################-----Main program that calls all the funcs---######################################
def algo_call():
    num, re, ge, ca, su, pr, du, sp, bu, p = Input()
    for i in range(0,num):
	n, reg, gen, cat, subcat, prof, dur, spo,  bud, prog= Input()
	url ="http://localhost:2770/compute-media-package"
	api = str(url)+'?regions='+reg+'&date=21-10-16&gender='+gen+'&category='+cat+'&sub_category='+subcat+'&profile='+prof+'&duration='+dur+'&spot_duration='+spo+'&budgets='+bud+'&user_id=radhika@amagi.com'
	start_time = time.time()
	re=requests.get(api)
	end_time = time.time()
	if (re.status_code != 200):
	    print re.status_code,',',api
	    logger.info('Status=%d,api=%s',int(re.status_code),api)
	    continue
	else:
#	    print api
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
		basic = basic_check(api,gen,spo,bud,g_out,spo_out,bud_out,tax_out,prof)
	    if prog == "All" or prog == "uu":
	        uu = UnderUtil(api,bud,bud_out,pkg_cost_out)
	    if prog == "All" or prog == "ap":
	        ap = apportioning_er(api,data,bud_out)
	    if prog == "All" or prog == "ch":
	        ch = valid_channels(api,data)
	    if prog == "All" or prog == "imp":
		imp = impressions(api,data,prof)
	    if prog == "All" or prog == "cr":
		cr = channel_reach(api,data,prof)
	    if prog == "All" or prog == "ra":
		ra = rationale(api,data)
#	    if prog == "All" or prog == "sr":
#		sr = spot_reach(api,data,prof)
	    if prog == "All" or prog == "er":
		eff_r = er(api,data)
	    print api
#	    return data
###########################################-----output data from json-----#############################################################################

def basic_check(api,gen,spo,bud,g_out,spo_out,bud_out,tax_out,prof):
    percent = round(15*(bud_out)/100)
    if ((str(gen) == str(g_out)) or ((str(gen) != str(g_out)) and (str(prof) == 'Kids' or str(prof) == 'All Adults'))) and (str(spo) == str(spo_out)) and (tax_out == percent or tax_out == (percent +1) or tax_out == (percent -1)):
	print 'Basic_Pass',',',
    else:
	print 'Basic_Fail',',',
	logger.info('Basic_Fail:Api=%s,gen=%s,g_out=%s,spo=%s,spo_out=%s,tax_out=%s,percent=%s',api,str(gen),str(g_out),str(spo),str(spo_out),str(tax_out),str(percent))
###########################################-----Budget Under Util-------###############################################################################     

def UnderUtil(api,bud,bud_out,pkg_cost_out):
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

def apportioning_er(api,data,bud_out):
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
    if (int(dis_pkg_cost) == int(total_ac_cost)) or (int(dis_pkg_cost) == (int(total_ac_cost) - 1)) or (int(dis_pkg_cost) == (int(total_ac_cost) + 1)):
	print 'Appor_Er_Pass',',',
    else:
	print 'Appor_Er_Fail',',',
	logger.info('Appor_Er_Fail:Api=%s,Discounted_package_cost=%d,Summation_calc=%d',api,int(dis_pkg_cost),int(total_ac_cost))
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
def valid_channels(api,data):
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
		    res1 = "Pass"
		elif enabled_value == 2 and reg_out == "National":
		    res1 = "Pass"
		else:
		    res1 = "Fail"
		    logger.info('Valid_chan_fail:Api=%s,reg=%s,chan=%s,enabled_val=%d',api,str(reg_out),str(chan_out),int(enabled_value))
	all_res = []
	all_res.append(res1)
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
def impressions(api,data,prof):
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
		if (int(imp_calc) == int(impressions_out)) or (int(impressions_out) == int(imp_calc)-1) or (int(impressions_out) == int(imp_calc)+1): 			 		    
		    res2 = "Pass"
		else:
		    res2 = "Fail"
            I = []
            I.append(res2)
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

def channel_reach(api,data,prof):
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
		if (int(chan_reach_calc) == int(chan_reach_out)) or (int(chan_reach_out) == int(chan_reach_calc)-1) or (int(chan_reach_out) == int(chan_reach_calc)+1):
		    res3 = 'Pass'
		else:
		    res3 = 'Fail'
#		print res3, int(chan_reach_calc), int(chan_reach_out)
	    C = []
	    C.append(res3)
    if (all(C[0] == item for item in C)) and (C[0] == 'Pass'):
	print 'CReach_pass',',',
    else:
	print 'CReach_fail',',',
	logger.info('Chan_Reach_Fail:Api=%s',api)
#####################################-------Sanity Rationale & Rationale message should be string---------###############################################################
def rationale(api,data):
    for i in range(0,len(data['package']['region'])):
        if data['package']['region'][i]['channel_order'] == []:
            continue
        else:
            for j in range(0,len(data['package']['region'][i]['channels'])):
#		print data['package']['region'][i]['channels'][j]['rationale']
                if ("rationale" in data['package']['region'][i]['channels'][j]) and ((isinstance((data['package']['region'][i]['channels'][j]['rationale']),(str,unicode))) == True):
                    res4 = "Pass"
                else:
                    res4 = "Fail"
	    R = []
            R.append(res4)
    if (all(R[0] == item for item in R)) and (R[0] == 'Pass'):
        print 'Rationale_pass',',',
    else:
        print 'Rationale_fail',',', 
	logger.info('Rationale_Fail:Api=%s,Rationale_message=%s',api,str(data['package']['region'][i]['channels'][j]['rationale']))

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
def spot_reach(api,data,prof):
    for i in range(0,len(data['package']['region'])):
        if data['package']['region'][i]['channel_order'] == []:
            continue
        else:
	    res5 = None
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
			if (int(spot_reach_out) == int(spot_reach_calc)) or (int(spot_reach_out) == int(spot_reach_calc)-1) or (int(spot_reach_out) == int(spot_reach_calc)+1):
			    res5 = 'Pass'
			else:
			    res5 = 'Fail'
			    logger.info('Spot_Reach_Fail:Api=%s,spot_reach_out=%s,spot_reach_calc=%s,I/Ps:reg=%s,chan=%s,age=%s,gendr=%s,nccs=%s,rotates_out=%s,coverage=%s,Percentage=%s,Spo_reach_mongo=%s',api,str(spot_reach_out),str(spot_reach_calc),str(reg_out),str(chan_out),str(age),str(g),str(nccs),str(rotates_out),str(coverage),str(val),str(sr1),str(sr2))
		    else:
			spot_reach_calc_1 = sr1 * (val / 100)
			spot_reach_calc_2 = sr2 * (val / 100)
			if (int(spot_reach_out) >= int(spot_reach_calc_1)) and (int(spot_reach_out) <= int(spot_reach_calc_2)):
			    res5 = 'Pass'
			else:
			    res5 = 'Fail'
			    logger.info('Spot_Reach_Fail:Api=%s,spot_reach_out=%s,spot_reach_range=%s,I/Ps:reg=%s,chan=%s,age=%s,gendr=%s,nccs=%s,rotates_out=%s,coverage=%s,Percentage=%s,Spo_reach_mongo=%s',api,str(spot_reach_out),str(spot_reach_calc_1),str(spot_reach_calc_2),str(reg_out),str(chan_out),str(age),str(g),str(nccs),str(rotates_out),str(coverage),str(val),str(sr1),str(sr2))
####Covering Non National channels######
                elif reg_out != "National":
                    coverage = chan_map_mongo(reg_out,type_out,chan_out)
                    val = reach_split_mongo(coverage,reg_out)
		    if sr1 == sr2:
                        spot_reach_calc = sr1 * (val / 100)
			if int(spot_reach_out) == int(spot_reach_calc) or (int(spot_reach_out) == int(spot_reach_calc)-1) or (int(spot_reach_out) == int(spot_reach_calc)+1):
			    res5 = 'Pass'
			else:
			    res5 = 'Fail'
			    logger.info('Spot_Reach_Fail:Api=%s,spot_reach_out=%s,spot_reach_calc=%s,I/Ps:reg=%s,chan=%s,age=%s,gendr=%s,nccs=%s,rotates_out=%s,coverage=%s,Percentage=%s,Spo_reach_mongo=%s',api,str(spot_reach_out),str(spot_reach_calc),str(reg_out),str(chan_out),str(age),str(g),str(nccs),str(rotates_out),str(coverage),str(val),str(sr1),str(sr2))
                    else:
                        spot_reach_calc_1 = sr1 * (val / 100)
                        spot_reach_calc_2 = sr2 * (val / 100)
                        if (int(spot_reach_out) >= int(spot_reach_calc_1)) and (int(spot_reach_out) <= int(spot_reach_calc_2)):
                            res5 = 'Pass'
                        else:
                            res5 = 'Fail'
			    logger.info('Spot_Reach_Fail:Api=%s,spot_reach_out=%s,spot_reach_range=%s,I/Ps:reg=%s,chan=%s,age=%s,gendr=%s,nccs=%s,rotates_out=%s,coverage=%s,Percentage=%s,Spo_reach_mongo=%s',api,str(spot_reach_out),str(spot_reach_calc_1),str(spot_reach_calc_2),str(reg_out),str(chan_out),str(age),str(g),str(nccs),str(rotates_out),str(coverage),str(val),str(sr1),str(sr2))
		if res5 == None:
		    res5 = 'Manually_check_SR'
		    continue
		S = []
		S.append(res5)	
    if (all(S[0] == item for item in S)) and (S[0] == 'Pass'):
	print 'SReach_pass',',',
    elif (all(S[0] == item for item in S)) and (S[0] == 'Manually check SR'):
	print 'Manually check SR'
    else:
	print 'SReach_fail',',',
#	print res5 , type_out, coverage, val, spot_reach_out, sr1 ,sr2

############################################################################################ Er check ######################################################################
#########Eff rate from mongo###################
def eff_rate_mongo(reg,chan):
    c = db.effective_rates.find({"channel":chan,"region":reg})
    for doc in c:
        eff_r = doc.get("effective_rate")
        return eff_r
##############################################
def er(api,data):
    answer_map = {}
    for i in range(0,len(data['package']['region'])):
        if data['package']['region'][i]['channel_order'] == []:
            continue
        else:
            for j in range(0, len(data['package']['region'][i]['channels'])):
                reg_out = data['package']['region'][i]['region_name']
		reg_cost = data['package']['region'][i]['region_cost']
                type_out = data['package']['region'][i]['channels'][j]['type']
		secondages = data['package']['region'][i]['channels'][j]['secondages']
                discounted_region_cost = data['package']['region'][i]['discounted_region_cost']
		spot_dur = data['package']['spot_duration']
#		print spot_dur
		chan_out = data['package']['region'][i]['channels'][j]['channel_name']
                eff_rate = data['package']['region'][i]['channels'][j]['effective_rate']
                cost = data['package']['region'][i]['channels'][j]['cost']
                actual_cost = data['package']['region'][i]['channels'][j]['actual_cost']
                rotates = data['package']['region'][i]['channels'][j]['rotates']
		if (reg_out == 'National' and type_out == 'National') or (reg_out != 'National' and type_out == 'Regional'):
		    Er_mongo = eff_rate_mongo(reg_out,chan_out)
		    Er_mongo_range = Er_mongo*1.1
		    cost_calc = float(Er_mongo)*int(rotates)*int(spot_dur)/10
		    cost_calc_range = float(Er_mongo_range)*int(rotates)*int(spot_dur)/10
                    ##Checking the range##
		    if ((int(cost) >= int(cost_calc)) and  (int(cost) <= int(round(cost_calc_range)))):
			resz = 'Pass'
#			print 'rz',resz
		    else:
			resz = 'Fail'
			logger.info('Er_Fail:Api=%s,I/Ps:reg_out=%s,chan_out=%s,type_out=%s, Er_mongo=%s,Er_mongo_range=%s,eff_rate=%s,cost_calc=%s,cost_calc_range=%s,cost=%s',api,str(reg_out),str(chan_out),str(type_out), str(Er_mongo),str(Er_mongo_range),str(eff_rate), str(cost_calc),str(cost_calc_range), str(cost))
#			print 'rz',resz
#		    print res6,reg_out,chan_out,type_out, Er_mongo, eff_rate, actual_cost_calc, 'range', range_actual_cost, actual_cost
#                   if actual_cost_r >= calc_actual_cost and actual_cost_r <= calc_1:
		elif type_out == 'Spliced':
		    package_data = data['package']
#		    answer_map = {}
		    for reg in package_data['region']:
			for chan in reg['channels']:
			    effective_rate = chan['effective_rate']
        		    secondages = chan['secondages']
        		    type_out = chan['type']
        		    region_out = reg['region_name']
        		    chan_out = chan['channel_name']
        		    rotates = chan['rotates']
        		    cost = chan['cost']
        		    actual_cost = chan['actual_cost']
        		    if type_out == 'Spliced':
				if chan_out in answer_map.keys():
				    answer_map[chan['channel_name']][reg['region_name']] = (effective_rate,rotates,cost,actual_cost)
            			else:
				    answer_map[chan['channel_name']] = {}
				    answer_map[chan['channel_name']][reg['region_name']] = (effective_rate,rotates,cost,actual_cost)
    
#    print 'answer_map',answer_map
    for y in answer_map.items():
#	print y
	y_chan = y[0]
	y_reg = list(y[1])
	if len(y_reg) == 1:
	    if y_reg[0] == 'National':
		Er_mongo = eff_rate_mongo("DTH",y_chan)
	    else:
		Er_mongo = eff_rate_mongo(y_reg[0],y_chan)
	    y_val = {}
	    y_val = y[1]
	    y_val1 = y_val[y_reg[0]]
	    y_val_list = list(y_val1)
#	    print y_val_list
	    effective_rate = y_val_list[0]
	    rotates_out = y_val_list[1]
	    cost = y_val_list[2]
	    actual_cost = y_val_list[3]
#	    print effective_rate, rotates_out, cost, actual_cost
	    cost_calc = float(Er_mongo)*int(rotates_out)*int(spot_dur)/10
	    actual_cost_calc = cost_calc/1.1
#	    print Er_mongo, rotates_out, cost_calc, actual_cost_calc 
	    if ((int(cost) == int(cost_calc)) or (int(cost) == int(cost_calc)-1) or (int(cost) == int(cost_calc)+1)) and ((int(actual_cost) == int(actual_cost_calc)) or (int(actual_cost) == int(actual_cost_calc)-1) or (int(actual_cost) == int(actual_cost_calc)+1)):
		resz = 'Pass'
#		print 'Pass'
	    else:
#		resz = 'Fail'
		logger.info('Er_Fail:Api=%s,effective_rate=%s,Er_mongo=%s,rotates_out=%s,spot_dur=%s,cost=%s,cost_calc=%s,actual_cost=%s,actual_cost_calc=%s',api,str(effective_rate),str(Er_mongo),str(rotates_out),str(spot_dur),str(cost),str(cost_calc),str(actual_cost),str(actual_cost_calc))
		print 'Fail'
	else:
#	    print 'y',y
#	    print 'y[0]',y[0],'y[1]',y[1]
	    n = []
	    for x in y[1]:
#		print 'x',x
		l= y[1][x]
		m = list(l)
		m.insert(4,y[0])
		m.insert(5,x) 
#		print 'ins_m',m
		n.append(m)
#	    print 'li',n
	    n.sort(key = lambda o:o[0], reverse = True)	
#	    print 'sort', n
	    com_rot = [ele[1] for ele in n]
#	    print "Common rotates", com_rot
	    sorted_rot = sorted(com_rot)
	    min_rot = sorted_rot[0]
	    q = len(sorted_rot)
	    actual_cost_summation = 0
	    actual_cost_calc_summation = 0
	    for q1 in range(0,q):
		if q1 == 0:
#		    print 'n[0],n[0][0]', n[0],n[0][0]
		    if n[q1][5] == "National":
		        Er_mongo = eff_rate_mongo("DTH",n[q1][4])
		    else:
		        Er_mongo = eff_rate_mongo(n[q1][5],n[q1][4])
		    cost = n[q1][2]
		    actual_cost = n[q1][3]
		    cost_calc = float(Er_mongo)*int(n[q1][1])*int(spot_dur)/10	
		    actual_cost_calc = cost_calc/1.1
#		    print q1,n[q1][0],Er_mongo, n[0][1], cost ,cost_calc,actual_cost, actual_cost_calc
		    if ((int(cost) == int(cost_calc)) or (int(cost) == int(cost_calc)-1) or (int(cost) == int(cost_calc)+1)) and ((int(actual_cost) == int(actual_cost_calc)) or (int(actual_cost) == int(actual_cost_calc)-1) or (int(actual_cost) == int(actual_cost_calc)+1)):
		        res6 = 'Pass'
#		        print res6
		    else:
		        res6 = 'Fail'
			logger.info('Er_fail:Api=%s,effective_rate=%s,Er_mongo=%s,rotates_out=%s,spot_dur=%s,cost=%s,cost_calc=%s,actual_cost=%s,actual_cost_calc=%s',api,str(n[q1][0]),str(Er_mongo),str(n[q1][1]),str(spot_dur),str(cost),str(cost_calc),str(actual_cost),str(actual_cost_calc))
#		        print res6
	        if q1 == 1:
#		    print 'n[1],n[1][0]',n[1],n[1][0]
		    if n[q1][5] == "National":
                        Er_mongo = eff_rate_mongo("DTH",n[q1][4])
                    else:
                        Er_mongo = eff_rate_mongo(n[q1][5],n[q1][4])
                    cost = n[q1][2]
                    actual_cost = n[q1][3]
		    Er_used = int(Er_mongo) / 1.1
                    cost_calc = float(Er_mongo)*int(n[q1][1])*int(spot_dur)/10
		    actual_cost_c = Er_used * ((abs(int(n[q1][1])) - int(min_rot)) + (min_rot * 0.75))
		    actual_cost_calc = actual_cost_c * int(spot_dur)/10
#                    print q1,n[q1][0],Er_mongo, n[q1][1],cost,cost_calc,actual_cost,actual_cost_calc
                    if ((int(cost) == int(cost_calc)) or (int(cost) == int(cost_calc)-1) or (int(cost) == int(cost_calc)+1)) and ((int(actual_cost) == int(actual_cost_calc)) or (int(actual_cost) == int(actual_cost_calc)-1) or (int(actual_cost) == int(actual_cost_calc)+1)):
                        res6 = 'Pass'
#                        print res6
                    else:
                        res6 = 'Fail'
			logger.info('Er_Fail:Api=%s,effective_rate=%s,Er_mongo=%s,Er_used=%s,rotates_out=%s,spot_dur=%s,cost=%s,cost_calc=%s,actual_cost=%s,actual_cost_calc=%s',api,str(n[q1][0]),str(Er_mongo),str(Er_used),str(n[q1][1]),str(spot_dur),str(cost),str(cost_calc),str(actual_cost),str(actual_cost_calc))
#                        print res6
		if q1 >= 2:
#		    print 'n[q],n[q][0]', n[q],n[q][0]
                    if n[q1][5] == "National":
                        Er_mongo = eff_rate_mongo("DTH",n[q1][4])
                    else:
                        Er_mongo = eff_rate_mongo(n[q1][5],n[q1][4])
                    cost = n[q1][2]
                    actual_cost = n[q1][3]
		    Er_used = int(Er_mongo) / 1.1
                    cost_calc = float(Er_mongo)*int(n[q1][1])*int(spot_dur)/10
                    actual_cost_c = Er_used * ((abs(int(n[q1][1])) - int(min_rot)) + (min_rot * 0.9))
		    actual_cost_calc = actual_cost_c * int(spot_dur)/10
 #                   print q1,n[q1][0], Er_mongo, n[q1][1],cost,cost_calc,actual_cost,actual_cost_calc
                    if ((int(cost) == int(cost_calc)) or (int(cost) == int(cost_calc)-1) or (int(cost) == int(cost_calc)+1)) and ((int(actual_cost) == int(actual_cost_calc)) or (int(actual_cost) == int(actual_cost_calc)-1) or (int(actual_cost) == int(actual_cost_calc)+1)):
                        res6 = 'Pass'
#                        print res6
                    else:
                        res6 = 'Fail'
			logger.info('Er_Fail:Api=%s,effective_rate=%s,Er_mongo=%s,Er_used=%s,rotates_out=%s,spot_dur=%s,cost=%s,cost_calc=%s,actual_cost=%s,actual_cost_calc=%s',api,str(n[q1][0]),str(Er_mongo),str(Er_used),str(n[q1][1]),str(spot_dur),str(cost),str(cost_calc),str(actual_cost),str(actual_cost_calc))
#                        print res6
		actual_cost_summation += actual_cost
		actual_cost_calc_summation += actual_cost_calc
		E = []
		E.append(res6)
		if (all(E[0] == ite for ite in E)) and (E[0] == 'Pass'):
		    resz = 'Pass'
		elif (int(actual_cost_summation) == int(actual_cost_calc_summation)) or (int(actual_cost_summation) == int(actual_cost_calc_summation)-1) or (int(actual_cost_summation) == int(actual_cost_calc_summation)+1):
		    resz = 'Pass'
		else:
		    resz = 'Fail'
		    logger.info('Er_check_fail:Api=%s,Same ers: actual_cost_summation=%s,actual_cost_calc_summation=%s',api,str(actual_cost_summation),str(actual_cost_calc_summation))
    if resz == 'Pass':
	print 'Er_Pass',',',
    else:
	print 'Er_Fail',',',
		                                                                                                                                                                                            
#####################################################################################################################################
call = algo_call()


#################################---------Default algo call if inputs are not passed-----###############################
##def default_algo_call():
#    print "Default alof call"
