from flask import Blueprint, render_template, request
from .weather import get_city_matches, get_weather_with_cache

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    city_matches = []
    error_message = None

    if request.method == 'POST':
        if 'choose_city' in request.form:
            # User picked a city from the list
            lat = request.form.get('lat')
            lon = request.form.get('lon')
            display_name = request.form.get('display_name')
            if lat and lon and display_name:
                weather_data = get_weather_with_cache(lat, lon, display_name)
            else:
                error_message = "Sorry, something went wrong with your city selection."
        else:
            # User submitted a city name
            city = request.form.get('city')
            if not city or not city.strip():
                error_message = "Please enter a city name."
            else:
                city_matches = get_city_matches(city)
                if len(city_matches) == 1:
                    # Only one match, get weather directly
                    match = city_matches[0]
                    weather_data = get_weather_with_cache(match['lat'], match['lon'], match['display_name'])
                    city_matches = []
                elif len(city_matches) == 0:
                    error_message = "Sorry, could not find weather for that city."

    print("Weather data to display:", weather_data)  # Debugging line to check weather_data
    return render_template('index.html', weather_data=weather_data, city_matches=city_matches, error_message=error_message)