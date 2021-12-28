from types import DynamicClassAttribute, MappingProxyType
from django.shortcuts import redirect, render
from collections import Counter
import pygal
from pygal.style import Style
from pygal.style import DefaultStyle
from .models import Bookmark

import json

#helper function designed to parse BFRO data
def parse_bfro_json():
    with open('bfro_reports.json') as bfro_jsonfile: 
        data = json.load(bfro_jsonfile)
    for index, item in enumerate(data):
        item['special_number'] = index
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
    result_count = 0
    for item in data:
        states = item.get('STATE')
        year = item.get('YEAR')
        year_as_str = str(year)

        if states == request.GET.get('s') or year_as_str == request.GET.get('y'):
            filtered_data.append(item)
            result_count+=1

    return filtered_data, result_count
    
def sightings(request):
    all_years_sorted = _sightings_year_parse(request)
    all_states_sorted = _sightings_states_parse(request)
    filtered_data, result_count = _sightings_filtered(request)
    bookmarked_special_number = Bookmark.objects.values('special_number')
    bookmarked_special_number_list = []

    for bookmark in bookmarked_special_number:
        bookmarked_special_number_list.append(bookmark['special_number'])
        
    context = {
        'sightings': filtered_data,
        'all_years': all_years_sorted,
        'all_states': all_states_sorted,
        'result_count': result_count,
        'bookmarked_special_number': bookmarked_special_number,
        'bookmarked_special_number_list': bookmarked_special_number_list
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

def _months():
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
    ### this code block reorder months into correct ortder ###
    month_list = list(occurance_of_month.items())
    month_order = [10,5,12,4,2,3,8,6,1,7,9,11]
    month_list = [month_list[i] for i in month_order]

    for month in month_list:  
        number_of_month_sightings = month[1]
        pie_chart.add(month[0], number_of_month_sightings)
    
    months_pie_svg = pie_chart.render_data_uri()

    return months_pie_svg

def _seasons():
    occurance_of_seasons, occurance_of_month = _parse_seasons_months()

    custom_style = Style(
        label_font_size = 10,
        tite_font_size = 24,
        colors=('#A6CEE3','#03B5AA','#A23E48','#E6BFCE')
    )    

    pie_chart = pygal.Pie(height=490, width=1200, style=custom_style)
    pie_chart.title = 'Number of Sightings Per Season'
    ### this code block reorder seasons into correct ortder ###
    sightings_per_season_list = list(occurance_of_seasons.items())
    sightings_per_season_reorder = [2,1,0,3]
    sightings_per_season_list = [sightings_per_season_list[i] for i in sightings_per_season_reorder]


    for season in sightings_per_season_list:
        number_of_season_sightings = season[1]
        print(number_of_season_sightings)
        pie_chart.add(season[0], number_of_season_sightings)

    seasons_pie_svg = pie_chart.render_data_uri()
    return seasons_pie_svg

def seasons(request):
    months_pie_svg = _months()
    seasons_pie_svg = _seasons()
    context = {
        'seasons_pie_svg': seasons_pie_svg,
        'months_pie_svg': months_pie_svg
    }

    return render(request, 'pages/seasons.html', context)
##### END SEASONS BLOCK #####


##### CREATE BOOKMARK BLOCK #####    
def create_bookmark(request):
    data = parse_bfro_json()
    
    special_number = int(request.POST.get('special_number'))
    for sighting in data:
        if special_number == sighting['special_number']:
            Bookmark.objects.create(
                year = sighting['YEAR'],
                season = sighting['SEASON'],
                month = sighting.get('MONTH', ''),
                state = sighting['STATE'],
                county = sighting['COUNTY'],
                location = sighting.get('LOCATION_DETAILS', ''),
                observed = sighting['OBSERVED'],
                special_number = sighting['special_number'],
                logged_by=request.user,	
            )

    return redirect('/sightings')
##### END CREATE BOOKMARK BLOCK #####



##### DELETE BOOKMARK BLOCK #####
def delete_bookmark(request, bookmark_id):
    bookmark = Bookmark.objects.get(id=bookmark_id)
    bookmark.delete()

    # Redirect to wherever they came from
    return redirect(request.META.get('HTTP_REFERER', '/'))
##### END DELETE BOOKMARK BLOCK #####


##### JOURNAL BLOCK #####
def journal(request):
    bookmarked_sightings = Bookmark.objects.order_by('year')
    count = 0
    for sighting in bookmarked_sightings:
        if sighting:
            count +=1
    context = {
        'bookmarked_sightings': bookmarked_sightings,
        'bookmarked_count': count
    }
    return render(request, 'pages/journal.html', context)
##### END JOURNAL BLOCK #####


#### ADD JOURNAL NOTES #####
def add_journal_note(request, bookmark_id):

    bookmark = Bookmark.objects.get(id=bookmark_id)
    bookmark.notes = request.POST['notes']
    bookmark.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))
#### END ADD JOURNAL NOTES #####

