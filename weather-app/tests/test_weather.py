import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from app.weather import get_city_matches, get_weather_by_coords

@patch('app.weather.requests.get')
def test_get_city_matches_one_match(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {'display_name': 'Atlanta, Georgia, USA', 'lat': '33.749', 'lon': '-84.388'}
    ]
    matches = get_city_matches('Atlanta')
    assert len(matches) == 1
    assert matches[0]['display_name'] == 'Atlanta, Georgia, USA'

@patch('app.weather.requests.get')
def test_get_city_matches_multiple_matches(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {'display_name': 'Georgetown, Guyana', 'lat': '6.8', 'lon': '-58.16'},
        {'display_name': 'Georgetown, Texas, USA', 'lat': '30.63', 'lon': '-97.68'}
    ]
    matches = get_city_matches('Georgetown')
    assert len(matches) == 2
    assert matches[0]['display_name'].startswith('Georgetown')

@patch('app.weather.requests.get')
def test_get_city_matches_no_match(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []
    matches = get_city_matches('Xyzabcnotacity')
    assert matches == []

@patch('app.weather.requests.get')
def test_get_city_matches_special_characters(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {'display_name': 'São Paulo, Brazil', 'lat': '-23.55', 'lon': '-46.63'}
    ]
    matches = get_city_matches('São Paulo')
    assert len(matches) == 1
    assert 'São Paulo' in matches[0]['display_name']

@patch('app.weather.requests.get')
def test_get_weather_by_coords_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'current_weather': {
            'temperature': 75,
            'windspeed': 10,
            'weathercode': 1
        }
    }
    weather = get_weather_by_coords('33.749', '-84.388', 'Atlanta, Georgia, USA')
    assert weather['city'] == 'Atlanta, Georgia, USA'
    assert weather['temperature'] == 75
    assert weather['windspeed'] == 10
    assert weather['weathercode'] == 1

@patch('app.weather.requests.get')
def test_get_weather_by_coords_no_weather(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}
    weather = get_weather_by_coords('0', '0', 'Nowhere')
    assert weather is None