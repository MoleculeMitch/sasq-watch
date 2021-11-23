from collections import Counter

from django.http import request
from apps.core.views import _years_lists
import numpy as np
import json
import pprint

def parse_bfro_json():
    with open('bfro_reports.json') as bfro_jsonfile: 
        data = json.load(bfro_jsonfile)
    return data

def _parse_years(): #years helper to parse json data
    data = parse_bfro_json()

    occurance_of_year = {}
    for dict in data:
        year = dict.get('YEAR')
        year_as_str = str(year)
        if year_as_str not in occurance_of_year and year_as_str.isdigit():
            occurance_of_year[year_as_str] = 0
        if year_as_str.isdigit():
            occurance_of_year[year_as_str] += 1

    pprint.pprint(occurance_of_year)

    return occurance_of_year

def _years_lists(): #years helper to create usable lists for pygal
    occurance_of_year = _parse_years()
    
    occurance_list = []
    year_list = []
    counter = 0
    for year,count in occurance_of_year.items():
        occurance_list.append(count)
        year_list.append(year)
        occurance_list.sort()
        year_list.sort()
        counter+=1

_years_lists()

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