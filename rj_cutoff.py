def cutoff_from_mongo(region_name, channel_name):
            # cutoff_rate from mongo
            mongo_entire = db.effective_rates.find({})
            for rates in mongo_entire:
                # print rates
                Erate = (rates['region'] + ',', rates['channel'] + ',', rates['cutoff_rate'])
                region_m = Erate[0][:-1]
                channel_m = Erate[1][:-1]
                if region_name == region_m and channel_name == channel_m:
		    print 'Cutoff_Regional_Natio', Erate[2]
                    return Erate[2]


	def eff_rate(region_name, channel_name):
            ##effective rate from mongo
            mongo_entire = db.effective_rates.find({})
            for rates in mongo_entire:
                Erate = (rates['region'] + ',', rates['channel'] + ',', rates['effective_rate'])
                region_m = Erate[0][:-1]
                channel_m = Erate[1][:-1]
                if region_name == region_m and channel_name == channel_m:
		    print 'Effec_spliced', Erate[2]
                    Eff = Erate[2]
		    ten_eff = Eff/1.1
		    return ten_eff
        def cutoff_rate_check():
            final_cost_compute = 0
            # cutoff_rate from mongo
            for o in range(0, len(data['package']['region'])):
                if data['package']['region'][o]['channel_order'] == []:
                    continue
                    # If channel_order is not empty, then compute the actual cost
                else:
                    sum_c = 0
                    for p in range(0, len(data['package']['region'][o]['channels'])):
                        channel_name = data['package']['region'][o]['channels'][p]['channel_name']
                        type_out = data['package']['region'][o]['channels'][p]['type']
                        region_name = data['package']['region'][o]['region_name']
                        if region_name == 'National' and (type_out == 'National' or type_out == 'Regional'):
                            region_name = data['package']['region'][o]['region_name']
                        elif region_name == 'National' and type_out == 'Spliced':
                            region_name = 'DTH'
                        else:
                            region_name = data['package']['region'][o]['region_name']
                        if type_out == 'Spliced':
                            E_value = eff_rate(region_name, channel_name)
                        else:
                            E_value = cutoff_from_mongo(region_name, channel_name)
                        #    print E_value
                        actual_compute = E_value * spot_duration_out / 10
                        rotates_out = data['package']['region'][o]['channels'][p]['rotates']
                        cost_compute = actual_compute * rotates_out
                        print 'region_name', region_name, 'channel_name', channel_name, 'type', type_out, 'E_value', E_value, 'actual_compute', actual_compute, 'rotates', rotates_out, 'cost_compute', cost_compute
                        sum_c += cost_compute
                        # print 'sum_c', sum_c
                final_cost_compute += sum_c
               # print 'final', final_cost_compute
            # print 'minimum_package_cost', data['package']['minimum_discounted_cost']
            min_pakg_cost = data['package']['minimum_discounted_cost']
            final = round(final_cost_compute)
            print 'Min_package_cost', ',', min_pakg_cost, ',', 'Final_computed', ',', final, ',',
	    if final == min_pakg_cost or min_pakg_cost == (final - 1) or min_pakg_cost == (final + 1):
		print 'Cutoff-Pass',',',
	    else:
		print 'Cutoff-Fail',',',
