import requests
import logging

logging.basicConfig(filename='weather_app.log', level=logging.INFO)

WEATHER_CODE_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

def get_city_matches(city):
    geo_url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}"
    geo_resp = requests.get(geo_url, headers={"User-Agent": "weather-app"})
    if geo_resp.status_code != 200 or not geo_resp.json():
        return []
    matches = []
    for geo_data in geo_resp.json():
        matches.append({
            'display_name': geo_data.get('display_name', city),
            'lat': geo_data['lat'],
            'lon': geo_data['lon']
        })
    return matches

def get_weather_by_coords(lat, lon, display_name):
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&temperature_unit=fahrenheit"
        f"&hourly=relative_humidity_2m"
        f"&daily=sunrise,sunset"
        f"&timezone=auto"
    )
    try:
        weather_resp = requests.get(weather_url)
        data = weather_resp.json()
        current = data.get('current_weather')
        humidity = None

        # Get sunrise and sunset for today
        sunrise = sunset = None
        if 'daily' in data and 'sunrise' in data['daily'] and 'sunset' in data['daily']:
            sunrise = data['daily']['sunrise'][0]
            sunset = data['daily']['sunset'][0]

        # Match humidity to the current weather time
        if current and 'hourly' in data and 'relative_humidity_2m' in data['hourly']:
            times = data['hourly'].get('time', [])
            humidities = data['hourly']['relative_humidity_2m']
            if times and humidities:
                try:
                    idx = times.index(current['time'])
                    humidity = humidities[idx]
                except (ValueError, KeyError):
                    humidity = humidities[0]  # fallback

        weathercode = current.get('weathercode') if current else None
        weatherdesc = WEATHER_CODE_DESCRIPTIONS.get(weathercode, "Unknown")

        if current:
            return {
                'city': display_name,
                'temperature': current.get('temperature'),
                'windspeed': current.get('windspeed'),
                'weathercode': weathercode,
                'weatherdesc': weatherdesc,
                'humidity': humidity,
                'sunrise': sunrise,
                'sunset': sunset
            }
        return None
    except Exception as e:
        logging.error(f"Exception in get_weather_by_coords: {e}")
        return None

# Caching function
import time
weather_cache = {}
CACHE_DURATION = 600  # 10 minutes

def get_weather_with_cache(lat, lon, display_name):
    cache_key = f"{lat},{lon}"
    now = time.time()
    if cache_key in weather_cache:
        data, timestamp = weather_cache[cache_key]
        if now - timestamp < CACHE_DURATION:
            print("Using cached weather data!")
            return data
    data = get_weather_by_coords(lat, lon, display_name)
    if data:
        weather_cache[cache_key] = (data, now)
    return data