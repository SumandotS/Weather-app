from django.shortcuts import render
import requests
from django.http import JsonResponse
from geopy.geocoders import Nominatim
from weather.forms import CityForm
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'weather/index.html')


def get_weather(request, city_name):
    api_key="b1fd6e14799699504191b6bdbcadfc35" 
    unit = "metric"
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units={unit}"

    response = requests.get(api_url)
    data = response.json()

    if data.get('cod') != 404:
        weather_data = {
            "location": data["name"],
            "temperature": data["main"]["temp"],
            "weatherType": data["weather"][0]["description"],
            "realFeel": data["main"]["feels_like"],
            "windSpeed": data["wind"]["speed"],
            "windDirection": data["wind"]["deg"],
            "visibility": data["visibility"] / 1000,
            "pressure": data["main"]["pressure"],
            "maxTemperature": data["main"]["temp_max"],
            "minTemperature": data["main"]["temp_min"],
            "humidity": data["main"]["humidity"],
        }
    else:
        weather_data = {"message": "city not found"}

    return JsonResponse(weather_data)

def get_coordinates(city):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    return None, None

@csrf_exempt
def weather_view(request):
    form = CityForm()
    weather_list = []
    city = ""

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            lat, lon = get_coordinates(city)
            if lat is not None and lon is not None:
                api_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,rain'
                response = requests.get(api_url)
                if response.status_code == 200:
                    weather_data = response.json()
                    hourly_data = weather_data.get("hourly", {})
                    times = hourly_data.get("time", [])
                    temperatures = hourly_data.get("temperature_2m", [])
                    humidities = hourly_data.get("relative_humidity_2m", [])
                    precipitation_probabilities = hourly_data.get("precipitation_probability", [])
                    rains = hourly_data.get("rain", [])

                    for i in range(len(times)):
                        weather_list.append({
                            "time": times[i],
                            "temperature": temperatures[i],
                            "humidity": humidities[i],
                            "precipitation_probability": precipitation_probabilities[i],
                            "rain": rains[i],
                        })

    return render(request, 'weather/hourly.html', {'form': form, 'weather_list': weather_list, 'city': city})

def get_weather_map(request):
    return render(request, "weather/map.html")

def get_weather_heatmap(request):
    return render(request, "weather/heatmap.html")

def get_about(request):
    return render(request,"weather/about.html")