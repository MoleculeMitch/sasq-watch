from collections import Counter
from apps.core.views import _years_lists
import numpy as np
import json
import pprint

def parse_bfro_json():
    with open('bfro_reports.json') as bfro_jsonfile: 
        data = json.load(bfro_jsonfile)
    return data

def _sightings_parse():
    data = parse_bfro_json()

    sightings_dict = {}
    for dict in data:
        year = dict.get('YEAR')
        season = dict.get('SEASON')
        month = dict.get('MONTH')
        state = dict.get('STATE')
        county = dict.get('COUNTY')
        location_details = dict.get('LOCATION_DETAILS')
        observed = dict.get('OBSERVED')
        data_tuple = (year, season, month, state, county, location_details, observed)

        if data_tuple not in sightings_dict:
            sightings_dict = {
                'year':year,
                'season':season,
                'month': month,
                'state':state,
                'county': county,
                'location_details': location_details,
                'observed': observed
            }
    pprint.pprint(sightings_dict)

_sightings_parse()




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