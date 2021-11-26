import json
import pprint

def parse_bfro_json():
    with open('bfro_reports.json') as bfro_jsonfile: 
        data = json.load(bfro_jsonfile)
    return data

def _parse_seasons_months(): #seasons helper to parse json data
    data = parse_bfro_json()

    occurance_of_seasons = {}
    occurance_of_month = {}
    for dict in data:
        season = dict.get('SEASON')
        month = dict.get('MONTH')

        if season not in occurance_of_seasons:
            occurance_of_seasons[season] = 0
        if season:
            occurance_of_seasons[season] += 1

        if month not in occurance_of_month:
            occurance_of_month[month] = 0
        if month:
            occurance_of_month[month] += 1

    return (occurance_of_seasons, occurance_of_month)

def seasons():
    occurance_of_seasons, occurance_of_month = _parse_seasons_months()
    sightings_per_season_list = list(occurance_of_seasons.items())
    sightings_per_season_reorder = [2,1,0,3]
    sightings_per_season_list = [sightings_per_season_list[i] for i in sightings_per_season_reorder]


    for season in sightings_per_season_list:
        number_of_season_sightings = season[1]
        print(number_of_season_sightings)
seasons()