import requests
import json
import argparse
import sys

# api key from https://home.openweathermap.org/api_keys
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_weather_data(city, unit='metric'):
    params = {
        'q' : city,
        'appid' : API_KEY,
        'units' :unit
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error getting data for {city}: {e}')
        return None

def view_weather(data, unit):        #view weather info in readable format
    if not data or data.get('cod') != 200:
        return False
    
    city = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    wind_speed = data['wind']['speed']
    weather_desc = data['weather'][0]['description'].title()
    humidity = data['main']['humidity']
    
    unit_symbol = 'c' if unit == 'metric' else 'f'
    wind_unit = 'm/s' if unit == 'metric' else 'mph'
    
    print(f'\nWeather in {city}, {country}: ')
    print(f'. Temperature: {temp}{unit_symbol}')
    print(f'. Wind Speed: {wind_speed} {wind_unit}')
    print(f'. Conditions: {weather_desc}')
    print(f'. Humidity: {humidity}%')
    print(f'-'*40)
    return True

def main():  #main application function
    parser = argparse.ArgumentParser(
        description='Weather Application',
        epilog='Example: weather_api.py --cities London,Paris --unit imperial'
    )
    parser.add_argument(
        'cities',
        required=True,
        help='Comma-separated list of cities )'
        
    )
    parser.add_argument(
        '--unit',
        choices=['metric', 'imperial'],
        default='metric',    
    )
    args = parser.parse_args()
    
    if not API_KEY or API_KEY == 'YOUR_API_KEY':
        print('Error: Please replase 'YOUR_API_KEY' with the actual OpenWeatherMap API')
        syt.exit(1)
    
    cities = [city.strip() for city in args.cities.split(',')]
    unit_name = 'Celsius' if args.unit == 'metric' else 'Fahrenheit'
    
    print(f'\n{'WEATHER REPORT ':=^60}')
    print(f'Units: {unit_name}\n')
    
    valid_cities = []
    for city in cities:
        data = fetch_weather_data(city, args.unit)
        if view_weather(data, arg.unit):
            valid_cities.append(city)
        
    if not valid_cities:
        print('\nNo valid weather data retrived. Please Check: ')
        print('- City names (try 'City,Country' format for ambigous names)')
        print('- Your internet connection')
        print('- Api key configuration' )
        print('\nFor help: 3.2.py --help')
        sys.exit(1)
        
if __name__==' __main__':
    main()
    
    

    
    