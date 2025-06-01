# Weather App

## Project Overview

The Weather App is a modern, user-friendly web application built with Flask. It allows users to enter a city name and fetches the current temperature, wind speed, and humidity using the Open-Meteo API. The app helps users quickly find weather information for any city, handles invalid city names gracefully, suggests possible matches for ambiguous city names, and logs all API responses to a file for debugging and record-keeping.

---

## Installation Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd weather-app
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage Guide

1. **Run the Flask app:**
   ```bash
   export FLASK_APP=app:create_app
   export FLASK_ENV=development
   flask run
   ```
   If port 5000 is busy, use:
   ```bash
   flask run --port=5001
   ```

2. **Open your browser and go to:**
   ```
   http://127.0.0.1:5000
   ```
   or (if using a different port):
   ```
   http://127.0.0.1:5001
   ```

3. **Enter a city name** in the input box and click "Get Weather".

---

## What is Displayed

- **Current Weather in [City Name]**
  - 🌡️ **Temperature** (°F)
  - 💨 **Wind Speed** (km/h)
  - 💧 **Humidity** (%)
  - 🌦️ **Weather Code** (with tooltip explanation)
- **Error Message** if the city is not found or weather data is unavailable.
- **Suggestions** for possible city matches if there are multiple results for the entered city name.
- **Animated clouds** and a responsive, modern interface.

---

## Example Output

```
Current Weather in Atlanta, Georgia, USA

🌡️ Temperature: 75°F
💨 Wind Speed: 10 km/h
💧 Humidity: 60%
🌦️ Weather Code: 1 (Mainly clear)
```

If the city is not found:
```
Sorry, could not find weather for that city.
```

If there are multiple matches:
```
Did you mean:
- Georgetown, Guyana
- Georgetown, Texas, USA
```

---

## Features

- Enter any city name to get current weather data.
- Displays temperature (°F), wind speed (km/h), humidity, and weather code with tooltip.
- Handles invalid or misspelled city names with user-friendly errors.
- Suggests possible city matches if there are multiple results.
- Logs all API responses and errors to a file for easy debugging.
- Responsive and modern UI with animated clouds and tooltips.

---

## Future Improvements

- Add weather icons and more detailed weather descriptions.
- Support for more weather parameters (e.g., precipitation, UV index).
- Allow users to search by country or region for more precise results.
- Add user authentication for saving favorite cities.
- Support for multiple languages.
- Deploy the app online for public access.

---

## License

MIT License

---

**Enjoy using the Weather App!**
