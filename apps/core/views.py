from django.shortcuts import render
from collections import Counter
import pygal
from pygal.style import Style
import json

def parse_bfro_json():
    return

#home page
def home(request):

    context = {

    }

    return render(request, 'pages/home.html', context)

#about page
def about(request):

    context = {

    }
    return render(request, 'pages/about.html', context)

#sightings page
def sightings(request):
    
    context = {
    
    }
    return render(request, 'pages/sightings.html', context)

#helper function for years
# def _years_decades(input_year):
    #skipping 0th go until end of list, colon means end of list
    # return input_year[:-1]
#years page

def years(request):
    with open('bfro_reports.json') as bfro_jsonfile:
        data = json.load(bfro_jsonfile)

    occurance_of_year = {}
    occurance_list = []
    year_list = []
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
            occurance_list.append(count)
            year_list.append(year)
            occurance_list.sort()
            year_list.sort()
    # print('this is the yearlist', year_list)
    #pygal line graph code block. shows the trend of sightings over the last 100 years
    custom_style = Style(
        label_font_size = 10,
        tite_font_size = 24,
    )
    line_chart = pygal.Line(x_label_rotation=90, style=custom_style,height = 490, width = 1200)
    line_chart.title = 'Sighting Chronology'
    line_chart.x_labels = year_list
    line_chart.add('Sightings',occurance_list)
    sightings_line_svg = line_chart.render_data_uri()
    context = {
        'stats': occurance_of_year,
        'count': count,
        'sightings_line_svg': sightings_line_svg
    }

    return render(request, 'pages/years.html', context)

#states page
def states(request):
    context = {
    }

    return render(request, 'pages/states.html', context)

#seasons page
def seasons(request):
    context = {
    }

    return render(request, 'pages/seasons.html', context)