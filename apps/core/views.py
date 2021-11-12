from django.shortcuts import render
from collections import Counter
import pygal
from pygal.style import Style
from pygal.style import DefaultStyle

import json


#helper function designed to parse BFRO data
def parse_bfro_json():
    with open('bfro_reports.json') as bfro_jsonfile: 
        data = json.load(bfro_jsonfile)
    return data



##### HOME BLOCK #####
def home(request):

    context = {

    }

    return render(request, 'pages/home.html', context)
##### END HOME BLOCK #####

##### ABOUT BLOCK #####
def about(request):

    context = {

    }
    return render(request, 'pages/about.html', context)
##### END ABOUT BLOCK#####

##### SIGHTINGS BLOCK #####
def sightings(request):
    
    context = {
    
    }
    return render(request, 'pages/sightings.html', context)
##### END SIGHTINGS BLOCK #####


##### YEARS BLOCK ######
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

    return occurance_of_year

def _years_lists(): #years helper to create usable lists for pygal
    occurance_of_year = _parse_years()
    
    occurance_list = []
    year_list = []

    for year,count in occurance_of_year.items():
        occurance_list.append(count)
        year_list.append(year)
        occurance_list.sort()
        year_list.sort()

    return (occurance_list, year_list)

def years(request): #years main function, renders pygal line chart
    occurance_list, year_list = _years_lists()

    custom_style = Style(
        label_font_size = 10,
        tite_font_size = 24,
    )
    line_chart = pygal.Line(x_label_rotation=90, style=custom_style, height = 490, width = 1200)
    line_chart.title = 'Sightings Per years'
    line_chart.x_labels = year_list
    line_chart.add('Sightings',occurance_list)
    sightings_line_svg = line_chart.render_data_uri()

    context = {
        'sightings_line_svg': sightings_line_svg
    }

    return render(request, 'pages/years.html', context)
##### END OF YEARS BLOCK #####


##### STATES BLOCK #####
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

    states_list = []
    sightings_list = []

    for states,sightings in states_dict.items():
        states_list.append(states)
        sightings_list.append(sightings)
    
    return (states_list, sightings_list)

def states(request):
    states_list, sightings_list = _states_lists()

    bar_chart = pygal.Bar(width = 1200, height = 490,x_label_rotation=90)
    bar_chart.title = 'Sightings Per State'
    bar_chart.x_labels = states_list
    bar_chart.add('Sightings', sightings_list)
    states_bar = bar_chart.render_data_uri()

    context = {
        'states_bar': states_bar,
    }

    return render(request, 'pages/states.html', context)
##### END STATES BLOCK #####


##### SEASONS BLOCK #####
def _parse_seasons(): #seasons helper to parse json data
    data = parse_bfro_json()

    occurance_of_seasons = {}
    for dict in data:
        season = dict.get('SEASON')
        if season not in occurance_of_seasons:
            occurance_of_seasons[season] = 0
        if season:
            occurance_of_seasons[season] += 1

    return occurance_of_seasons


def seasons(request):
    occurance_of_seasons = _parse_seasons()
    fall = occurance_of_seasons["Fall"]
    summer = occurance_of_seasons['Summer']
    spring = occurance_of_seasons['Spring']
    winter = occurance_of_seasons['Winter']

    pie_chart = pygal.Pie(height = 490, width = 1200)
    pie_chart.title = 'Sightings Per Season'
    pie_chart.add('Fall', fall)
    pie_chart.add('Summer', summer)
    pie_chart.add('Spring', spring)
    pie_chart.add('Winter', winter)
    seasons_pie_svg = pie_chart.render_data_uri()

    context = {
        'seasons_pie_svg': seasons_pie_svg
    }

    return render(request, 'pages/seasons.html', context)
##### END SEASONS BLOCK #####