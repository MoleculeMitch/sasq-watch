from collections import Counter
import numpy as np
import json
import pprint

def parse_bfro_json():
    with open('bfro_reports.json') as bfro_jsonfile: 
        data = json.load(bfro_jsonfile)
    return data

    ##### SEASONS BLOCK #####
def _states_parse(): #seasons helper to parse json data
    data = parse_bfro_json()
    
    states_dict = {}
    for dict in data:
        state = dict.get('STATE')
        if state not in states_dict:
            states_dict[state] = 0
        if state:
            states_dict[state] += 1

    return states_dict

def _states_lists():
    states_dict = _states_parse()
    # pprint.pprint(states_dict)
    states_list = []
    sightings_list = []

    for states,sightings in states_dict.items():
        states_list.append(states)
        sightings_list.append(sightings)

    return(states_list, sightings_list)
    
def states():
    states_list, sightings_list = _states_lists()

    pprint.pprint(states_list)
    pprint.pprint(sightings_list)

states()

######practice turnig string numbers to numbers, then numbers to decades######
# years_nums = []
# for years_as_nums in year_list:
#     test=int(years_as_nums)
#     years_nums.append(test)
# # print(years_nums)


# years=np.array(years_nums)
# decades = []
# for year in years:
#     decade = int(np.floor(year / 10) * 10)
#     decades.append(decade)
# decades.sort()
# print(f'numpy example {decades}') 
#### this practice block is a successs ####