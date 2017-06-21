import json
from pprint import pprint
import operator

with open('/home/ubuntu/.gvm/pkgsets/go1.6/dsp/src/github.com/amagimedia/mix-algs/sample1.json') as data_file:
    data = json.load(data_file)

package_data = data['package']

answer_map = {}

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
	if region_out != 'National' and type_out == 'Spliced':
	    if chan_out not in answer_map.keys():
		answer_map[chan['channel_name']] = {}
		answer_map[chan['channel_name']][reg['region_name']] = (effective_rate, secondages)
		
            if chan_out in answer_map.keys():
                answer_map[chan['channel_name']][reg['region_name']] = (effective_rate, secondages)
	    else:
                answer_map[chan['channel_name']] = {}
                answer_map[chan['channel_name']][reg['region_name']] = (effective_rate, secondages)
			

print answer_map



final_answer_map = {}

for channel, regions in answer_map.iteritems():
    final_answer_map[channel] = sorted(regions.items(), key=operator.itemgetter(1), reverse=True)

print final_answer_map
