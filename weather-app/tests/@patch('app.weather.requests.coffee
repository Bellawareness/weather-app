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