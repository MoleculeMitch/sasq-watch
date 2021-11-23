from types import MappingProxyType
from django.shortcuts import render
from collections import Counter
import pygal
from pygal.style import Style
from pygal.style import DefaultStyle
import pprint

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
def _sightings_year_parse(request):
    data = parse_bfro_json()

    all_years = {}
    all_years_sorted = []

    for item in data:
        year = item.get('YEAR')
        year_as_str = str(year)
        if year_as_str not in all_years and year_as_str.isdigit():
            all_years[year_as_str] = 0
        if year_as_str.isdigit():
            all_years[year_as_str] += 1

    for year, count in all_years.items():
        all_years_sorted.append(year)
        all_years_sorted.sort()

    return all_years_sorted

def _sightings_states_parse(request):
    data = parse_bfro_json()

    all_states = {}
    all_states_sorted = []

    for item in data:
        states = item.get('STATE')
        if states not in all_states:
            all_states[states] = 0
        if all_states:
            all_states[states] += 1


    for state, count in all_states.items():
        all_states_sorted.append(state)
        all_states_sorted.sort()

    return  all_states_sorted

def _sightings_filtered( request):
    data = parse_bfro_json()

    filtered_data = []

    for item in data:
        states = item.get('STATE')
        year = item.get('YEAR')
        year_as_str = str(year)

        if states == request.GET.get('s'):
            filtered_data.append(item)

        if year_as_str == request.GET.get('y'):
            filtered_data.append(item)

    return filtered_data
    
def sightings(request):
    all_years_sorted = _sightings_year_parse(request)
    all_states_sorted = _sightings_states_parse(request)
    filtered_data = _sightings_filtered(request)

    context = {
        'sightings': filtered_data,
        'all_years': all_years_sorted,
        'all_states': all_states_sorted,
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
    occurance_year_sorted = list(occurance_of_year.items())
    occurance_year_sorted.sort()

    for year,count in occurance_year_sorted:
        occurance_list.append(count)
        year_list.append(year)

    return (occurance_list, year_list)

def years(request): #years main function, renders pygal line chart
    occurance_list, year_list = _years_lists()

    custom_style = Style(
        label_font_size = 10,
        tite_font_size = 24,
        colors=('#03B5AA',)
    )
    line_chart = pygal.Line(x_label_rotation=90, style=custom_style, height = 490, width = 1200)
    line_chart.title = 'Number of Sightings Per year'
    line_chart.x_labels = year_list
    line_chart.add('Sightings',occurance_list)
    sightings_line_svg = line_chart.render_data_uri()

    context = {
        'sightings_line_svg': sightings_line_svg
    }

    return render(request, 'pages/years.html', context)
##### END OF YEARS BLOCK #####


##### STATES BLOCK #####
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
 
    custom_style = Style(
        label_font_size = 10,
        tite_font_size = 24,
        colors=('#A23E48',)
    )
 
    bar_chart = pygal.Bar(width=1200, height=490, x_label_rotation=90, style=custom_style)
    bar_chart.title = 'Number of Sightings Per State'
    bar_chart.x_labels = states_list
    bar_chart.add('Sightings', sightings_list)
    states_bar = bar_chart.render_data_uri()

    context = {
        'states_bar': states_bar,
    }

    return render(request, 'pages/states.html', context)
##### END STATES BLOCK #####


##### SEASONS BLOCK #####
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

def months():
    occurance_of_seasons, occurance_of_month = _parse_seasons_months()

    custom_style = Style(
        label_font_size = 10,
        tite_font_size = 24,
        colors=('#A6CEE3','#03B5AA','#A23E48','#E6BFCE',
                '#B5BA72','#93E1D8','#FF521B','#109648',
                '#706C61','#462255','#FC9E4F','#087E8B'
                )
    )

    pie_chart = pygal.Pie(height=490, width=1200, style=custom_style)
    pie_chart.title = 'Number of Sightings Per Month'

    
    for month in occurance_of_month:
        number_of_month_sightings = occurance_of_month[month]
        pie_chart.add(month, number_of_month_sightings)

    months_pie_svg = pie_chart.render_data_uri()

    return months_pie_svg

def seasons(request):
    occurance_of_seasons, occurance_of_month = _parse_seasons_months()
    months_pie_svg = months()

    custom_style = Style(
        label_font_size = 10,
        tite_font_size = 24,
        colors=('#A6CEE3','#03B5AA','#A23E48','#E6BFCE')
    )    

    pie_chart = pygal.Pie(height=490, width=1200, style=custom_style)
    pie_chart.title = 'Number of Sightings Per Season'

    for season in occurance_of_seasons:
        if season == 'Unknown':
            continue
        number_of_season_sightings = occurance_of_seasons[season]
        pie_chart.add(season, number_of_season_sightings)

    seasons_pie_svg = pie_chart.render_data_uri()

    context = {
        'seasons_pie_svg': seasons_pie_svg,
        'months_pie_svg': months_pie_svg
    }

    return render(request, 'pages/seasons.html', context)
##### END SEASONS BLOCK #####