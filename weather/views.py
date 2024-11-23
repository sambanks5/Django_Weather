from django.shortcuts import render
import requests

def index(request):
    geocode_url = 'http://api.openweathermap.org/geo/1.0/direct'
    onecall_url = 'https://api.openweathermap.org/data/3.0/onecall'
    google_maps_api_key = 'AIzaSyBbimgoCedgG-tMRK5CGrFGcG-uYfEP91M'
    api_key = '7b9718d8f06cd8c26c2ac9b9c3daaf79' 

    city = request.GET.get('city', '')
    lat = request.GET.get('lat', '')
    lon = request.GET.get('lon', '')
    

    if not city and not (lat and lon):
        context = {
            'error': 'No city name entered.'
        }
        return render(request, 'weather/index.html', context)

    if city:
        geocode_params = {
            'q': city,
            'appid': api_key
        }
        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_data = geocode_response.json()

        if geocode_data:
            lat = geocode_data[0]['lat']
            lon = geocode_data[0]['lon']
        else:
            context = {
                'error': 'City not found.'
            }
            return render(request, 'weather/index.html', context)

    onecall_params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'minutely,hourly', 
        'appid': api_key,
        'units': 'metric'
    }

    onecall_response = requests.get(onecall_url, params=onecall_params)
    weather_data = onecall_response.json()

    # Generate Google Maps Static API URL
    google_maps_url = (
        f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=10&size=1000x800&scale=2"
        f"&style=feature:all|element:labels|visibility:off&key={google_maps_api_key}"
    )
    context = {
        'city': city if city else 'Your Location',
        'weather_data': weather_data,
        'lat': lat,
        'lon': lon,
        'google_maps_url': google_maps_url,
    }
    return render(request, 'weather/index.html', context)