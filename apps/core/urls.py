from django.urls import path

from apps.core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sightings/', views.sightings, name='sightings'),
    path('years/', views.years, name='years'),
    path('states/', views.states, name='states'),
    path('seasons/', views.seasons, name='seasons')
]
