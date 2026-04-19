# 🌦️ Weather App CLI

A Python command-line application for checking current weather conditions and a multi-day forecast for one or more cities using the Open-Meteo API.

## 📌 Overview

This project accepts one or more city names, converts each name into geographic coordinates, and then queries both current conditions and the daily forecast to display a clear summary in the terminal.

Main flow:

1. Read a list of cities entered by the user.
2. Look up the latitude and longitude for each city with the Open-Meteo Geocoding API.
3. Fetch the current weather and a 5-day forecast from the Forecast API.
4. Display a comparison table across cities.
5. Show temperature, humidity, wind speed, precipitation, weather description, and daily forecast details.
6. Save responses to a local file when logging is enabled.
7. Reuse cached data when it is still valid for up to 1 hour.

## ✨ Highlights

- Simple and objective terminal interface.
- Automatic coordinate lookup by city name.
- Support for multiple cities in a single run.
- Side-by-side comparison in a table layout.
- Display of temperature, humidity, wind speed, and precipitation.
- 5-day forecast with highs and lows.
- Basic translation of `weathercode` values into readable descriptions.
- Error handling for invalid input, city not found, and connection failures.
- Local cache with a 1-hour lifetime.
- Modular structure with automated tests.

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- `pip`

### Steps

```bash
git clone <YOUR_REPOSITORY_URL>
cd weather-app/src
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 🚀 Usage

Run:

```bash
python main.py
```

Then enter the desired city name in the terminal.

You can enter multiple cities separated by commas.

## 🖥️ Example Output

```text
Enter one or more cities separated by commas: Sao Paulo, Rio de Janeiro

City comparison
+----------------+--------+----------+------------+---------+----------------+--------------+
| City           | Temp.  | Humidity | Wind       | Precip. | Condition      | Source       |
+----------------+--------+----------+------------+---------+----------------+--------------+
| Sao Paulo      | 24.1 C | 78 %     | 12.3 km/h  | 0.4 mm  | Partly cloudy  | API Open-Meteo |
| Rio de Janeiro | 28.0 C | 70 %     | 9.8 km/h   | 0.0 mm  | Clear sky      | local cache  |
+----------------+--------+----------+------------+---------+----------------+--------------+

================================================
Current weather - Sao Paulo
================================================
Data source: API Open-Meteo
Temperature: 24.1 C
Humidity: 78 %
Wind speed: 12.3 km/h
Precipitation: 0.4 mm
Condition: Partly cloudy
Updated at: 2026-04-17T21:00

Forecast for the next few days - Sao Paulo
+------------+--------+--------+
| Date       | High   | Low    |
+------------+--------+--------+
| 2026-04-18 | 26.0 C | 18.0 C |
| 2026-04-19 | 27.0 C | 19.0 C |
+------------+--------+--------+
```

## ⚙️ Features

- Current weather lookup by city name
- Processing of multiple cities in the same execution
- Automatic geocoding through Open-Meteo
- Side-by-side comparison table for cities
- Display of temperature, humidity, wind speed, and precipitation
- 5-day forecast with daily highs and lows
- Terminal-friendly formatted output
- Clearer error messages
- Response logging to `weather_log.jsonl` when enabled
- Local caching in `weather_cache.json`

## 🔒 Privacy and Local Storage

This project does not use an API key and does not request device GPS access. The location used in each lookup is inferred only from the city name typed by the user.

By default:

- Local caching is enabled in `weather_cache.json` for up to 1 hour.
- Detailed logging is disabled to reduce unnecessary persistence of lookup history.

If you want to change this behavior, configure environment variables before running:

```powershell
$env:WEATHER_APP_ENABLE_CACHE="1"
$env:WEATHER_APP_ENABLE_LOGGING="0"
python main.py
```

Accepted values: `1`, `true`, `yes`, `on`, `0`, `false`, `no`, `off`.

If you share this project or run it on a third-party machine, treat `weather_cache.json` and `weather_log.jsonl` as local usage and history data.

## 🧯 Error Handling

The app handles the most common cases:

- Empty input
- City not found
- Connection failure or HTTP error
- Incomplete API response

When one city fails, the others are still processed.

If a valid cache entry exists for a city, the app can respond without making a new API request.

## 📝 File Logging

Each successful lookup can be saved to `weather_log.jsonl` in JSON Lines format when logging is enabled.

This file can be used to:

- Keep a simple lookup history
- Inspect API responses
- Serve as a base for future analysis

## ⚡ Data Cache

The project stores lookups in `weather_cache.json` and reuses the data for up to 1 hour when `WEATHER_APP_ENABLE_CACHE` is enabled.

This helps:

- Reduce redundant API calls
- Improve response time for recently queried cities
- Demonstrate a practical feature often found in real applications

## 🌐 API Information

This project uses [Open-Meteo](https://open-meteo.com/) as its data source.

### Endpoints used

- `https://geocoding-api.open-meteo.com/v1/search`
- `https://api.open-meteo.com/v1/forecast`

### Fields used

- `latitude`
- `longitude`
- `temperature_2m`
- `relative_humidity_2m`
- `wind_speed_10m`
- `precipitation`
- `weathercode`
- `time`
- `temperature_2m_max`
- `temperature_2m_min`

## 📄 Licenses and Attribution

- Python dependency: `requests`, licensed under Apache 2.0
- Weather data: Open-Meteo, with API data licensed under CC BY 4.0
- Open-Meteo terms of use: the free plan applies to non-commercial usage, subject to the provider's published limits and conditions

Official details and links are available in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## 📁 Project Structure

```text
src/
|-- main.py
|-- geocoding.py
|-- weather.py
|-- display.py
|-- cache.py
|-- logger.py
|-- config.py
|-- tests/
|   |-- test_weather_app.py
|-- requirements.txt
|-- README.md
|-- THIRD_PARTY_NOTICES.md
|-- .gitignore
```

## ✅ Tests

The project includes automated test scenarios built with `unittest`.

To run them:

```bash
python -m unittest tests.test_weather_app
```

Covered scenarios:

- Parsing a comma-separated city list
- Handling empty input
- Successful processing of a valid city
- Handling an unknown city without interrupting the flow
- Logging during successful processing
- Validation of incomplete current weather data
- Validation of incomplete daily forecast data
- Cache key normalization

## 🔮 Future Improvements

- Accept command-line arguments
- Store recent lookups
- Export comparisons to CSV
- Allow cache lifetime configuration
- Build a GUI or web version

## 💻 Technologies

- Python
- Requests
- Open-Meteo API
- Unittest

## 👨‍💻 Author

Project created by **Rafael Alves**.

- GitHub: [rafael-alves-teixeira](https://github.com/rafael-alves-teixeira)
- Portfolio: [rafael-alves-teixeira.github.io/portfolio](https://rafael-alves-teixeira.github.io/portfolio/)
