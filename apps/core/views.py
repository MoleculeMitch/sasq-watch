from django.shortcuts import render
from collections import Counter
import json

def parse_bfro_json():
    return

# Two example views. Change or delete as necessary.
def home(request):

    context = {
        'example_context_variable': 'Change me.',
    }

    return render(request, 'pages/home.html', context)

def about(request):
    context = {
    }

    return render(request, 'pages/about.html', context)

def sightings(request):
    with open('bfro_reports.json') as bfro_jsonfile:
        data = json.load(bfro_jsonfile)

    occurance_of_year = {}
    count = 0
    for object in data:
        year = object.get('YEAR')
        year_as_str = str(year)
        if year_as_str not in occurance_of_year and year_as_str.isdigit():
            occurance_of_year[year_as_str] = 0
        if year_as_str.isdigit():
            occurance_of_year[year_as_str] += 1
            count += 1

    context = {
        'stats': occurance_of_year,
        'count': count
    }
    return render(request, 'pages/sightings.html', context)

def years(request):
    context = {
    }

    return render(request, 'pages/years.html', context)

def states(request):
    context = {
    }

    return render(request, 'pages/states.html', context)

def seasons(request):
    context = {
    }

    return render(request, 'pages/seasons.html', context)