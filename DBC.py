import commands
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
import requests, json
import sys
import urllib
global a,b
	
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp

def db_check():
	regions = db.channel_mappings.distinct("region",{"enabled":1})
	for i in range(0,len(regions)):
#		print i
		r = '\"'+regions[i]+'\"'
		print r
		channels = []
		channels = db.channel_mappings.find({"region":regions[i]})
		b = ''
		for j in channels:
#			if j.get("enabled") == 0:
#				continue
			if j.get("enabled") != 1: 
				chan = j.get("channel_name") 
				print chan
				type_o = j.get("type")
#				print type_o
				min_spots = db.channel_min_max_rotates_day.find({"channel":chan})
				for k in min_spots:
					min_m = k.get("min")
					#spot duration is 10
					min_final = min_m * 10
					#secondages
					secondages = str( min_final * 10)
					s = secondages
#					print s
					a = '{"channel_name":"'+ chan +'","secondages":'+ s +',"type":"'+ type_o +'"},'
#					print a
			b += a
			c = b[:-1]
#		print c
#		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		url = "http://stagingapi.amagimix.com/get-package-cost"
		url1 = "http://stagingapi.amagimix.com/login"
		payload1 = '{"email":"radhika@amagi.com","password":"amagi@123"}'
		headers1 = {'content-type': 'application/json'} 
		res = requests.post(url1, data=payload1, headers=headers1)
		rep = res.text
		d = json.loads(rep)
		token = d['data']['user_token']
		headers = {'content-type': 'application/json','Authorization':token}
		payload = '{"_id":2135,"channels":[' + c +'],"combos":[],"region_name":'+r+',"spot_duration":10,"prev_package_id":"588600078b27730441d96815"}'
		print payload 
		re = requests.post(url, data=payload, headers=headers)
		print re
		if str(re) == '<Response [200]>':
			print "Pass"
		else:
			print "False"
ch = db_check()
