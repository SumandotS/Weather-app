from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('weather/<str:city_name>', views.get_weather, name='get_weather'),
    path('hourly', views.weather_view, name='hourly_view'),
    path('weather-map', views.get_weather_map, name='weather_map'),
    path('weather-heatmap', views.get_weather_heatmap, name='weatherheat_map'),
    path('about', views.get_about, name='about-weatherapp'),
    
]


