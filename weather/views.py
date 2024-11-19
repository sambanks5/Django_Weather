from django.shortcuts import render
import requests

def index(request):
    geocode_url = 'http://api.openweathermap.org/geo/1.0/direct'
    onecall_url = 'https://api.openweathermap.org/data/3.0/onecall'
    api_key = '7b9718d8f06cd8c26c2ac9b9c3daaf79' 

    city = request.GET.get('city', '')
    if city == '':
        context = {
            'error': 'Please enter a city name.'
        }
        return render(request, 'weather/index.html', context)

    geocode_params = {
        'q': city,
        'appid': api_key
    }
    geocode_response = requests.get(geocode_url, params=geocode_params)
    geocode_data = geocode_response.json()

    if geocode_data:
        lat = geocode_data[0]['lat']
        lon = geocode_data[0]['lon']

        onecall_params = {
            'lat': lat,
            'lon': lon,
            'exclude': 'minutely,hourly', 
            'appid': api_key,
            'units': 'metric'
        }
        onecall_response = requests.get(onecall_url, params=onecall_params)
        weather_data = onecall_response.json()
    else:
        weather_data = None

    context = {
        'city': city,
        'weather_data': weather_data,
        'lat': lat,
        'lon': lon,
    }
    return render(request, 'weather/index.html', context)