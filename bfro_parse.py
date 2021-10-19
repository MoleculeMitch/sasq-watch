from collections import Counter
import json


#this function is a function to help parse out bad or messy data
with open('bfro_reports.json') as bfro_jsonfile:
        data = json.load(bfro_jsonfile)

year_count = []
for object in data:
    year = object.get('YEAR')
    year = str(year)
    if year.isdigit():
        year_count.append(year)
    print(year_count)
        

        


#idea about how to save the date
# if year is year.substring():
#     then cut the last part of the year
#     and cut any is alpha()


# bfro = open('bfr.txt').read()
# thing_to_remove = '{"REPORT_NUMBER": null, "REPORT_CLASS": null},'
# bfro_remove = bfro.replace(thing_to_remove, '')
# open('new_json.txt', 'w').write(bfro_remove)  