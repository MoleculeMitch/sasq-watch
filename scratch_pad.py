from collections import Counter
import numpy as np
import json


#this function is a function to help parse out bad or messy data
with open('bfro_reports.json') as bfro_jsonfile:
        data = json.load(bfro_jsonfile)

occurance_of_year = {}
occurance_list = []
year_list = []
total_occurance_list = []
count = 0
for object in data:
    year = object.get('YEAR')
    year_as_str = str(year)
    if year_as_str not in occurance_of_year and year_as_str.isdigit():
        occurance_of_year[year_as_str] = 0
    if year_as_str.isdigit():
        occurance_of_year[year_as_str] += 1
        count += 1

#pygal line graph accepts list only; make list
for year,count in occurance_of_year.items():
    year_list.append(year)
    occurance_list.sort()
    year_list.sort()
# print(f' this is the year list, {year_list}')





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