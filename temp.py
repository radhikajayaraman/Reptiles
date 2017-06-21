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
global a,b
	
with open("/var/chandni-chowk/configs/app.development.toml") as conffile:
    config = toml.loads(conffile.read())
mongo_client = MongoClient(config["app"]["mongo_conn_str"])
db = mongo_client.dsp

def db_check():
#	regions = ["National","DTH","Delhi NCR","Hyderabad","Bangalore","TN/Pondicherry","Kerala","Pun/Har/Cha/HP/J&K","Uttar Pradesh","West Bengal","North East","Orissa","Jharkhand","Bihar","Maharashtra/Goa","Chhattisgarh","Rajasthan","Madhya Pradesh"]
	regions = ["National","DTH"]
#	b = ''
	for i in range(0,len(regions)):
#		print i
		r = '\"'+regions[i]+'\"'
		print r
		channels = []
		channels = db.channel_mappings.find({"region":regions[i]})
		b = ''
		for j in channels:
			if j.get("enabled") != 0: 
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
		token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0ODU5MzQ4MTYsImlhdCI6MTQ4NTMzMDAxNiwic3ViIjoiOWMxY2YzMzUtOTM0ZS00MTBkLWJmYTEtODkwMmQ5MDZjMmFjIn0.m2o2SrlMJuWZXZ9_cxcnNiU1GpRbO1tX3x6osOP7bJqh__NHqJ7lSZhsxxEPeFlH3jtPptYpkvZAYXqXQaAsqBpV-8-IvMG-MpV0pKJjpu4TANqIinQmm6t2DDwfEXfdPrja19mtLpzpStJX17hDHLjgLmOWBu-wfJCR9Z5bdoM'
		headers = {'content-type': 'application/json','Authorization':token}
		payload = '{"_id":2135,"channels":[' + c +'],"combos":[],"region_name":'+r+',"spot_duration":10,"prev_package_id":"588600078b27730441d96815"}'
		print payload 
		re = requests.post(url, data=payload, headers=headers)
		print re
#		if re == 200:
#			print "Pass"
#		else:
#			print "False"
#	return c
ch = db_check()
#print ch
#payload = '{"_id":2149,"channels":[{"channel_name":"Zee News","secondages":930,"type":"Spliced"},{"channel_name":"Times Now","secondages":2120,"type":"Spliced"},{"channel_name":"CNBC Awaaz","secondages":2180,"type":"Spliced"},{"channel_name":"Zoom","secondages":2120,"type":"Spliced"},{"channel_name":"Zee Cinema","secondages":850,"type":"Spliced"},{"channel_name":"Magicbricks Now","secondages":2120,"type":"Spliced"},{"channel_name":"Colors","secondages":280,"type":"Spliced"},{"channel_name":"Romedy Now","secondages":2120,"type":"Spliced"},{"channel_name":"ET Now","secondages":2120,"type":"Spliced"},{"channel_name":"Movies Now","secondages":2120,"type":"Spliced"},{"channel_name":"IBN7","secondages":450,"type":"Spliced"},{"channel_name":"India News Rajasthan","secondages":2160,"type":"Regional"},{"channel_name":"Zee Marudhara","secondages":750,"type":"Regional"},{"channel_name":"ETV Rajasthan","secondages":2160,"type":"Regional"}],"combos":[],"region_name":"Rajasthan","spot_duration":10,"prev_package_id":"588f39628b27735ea3032e71"}'
#re = requests.post(url, data=payload, headers=headers)

#ch = chann_type("National")
#print ch
