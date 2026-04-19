import requests
from typing import TypedDict

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 10
CURRENT_FIELDS = (
    "temperature_2m,relative_humidity_2m,wind_speed_10m,weathercode,precipitation"
)
DAILY_FIELDS = "temperature_2m_max,temperature_2m_min"


class WeatherData(TypedDict):
    """Structured weather data returned by the Open-Meteo current forecast endpoint."""

    temperature_2m: float
    relative_humidity_2m: float
    wind_speed_10m: float
    precipitation: float
    weathercode: int
    time: str


class ForecastData(TypedDict):
    """Daily forecast block returned by the Open-Meteo forecast endpoint."""

    time: list[str]
    temperature_2m_max: list[float]
    temperature_2m_min: list[float]


class WeatherBundle(TypedDict):
    """Combined weather payload used by the application."""

    current: WeatherData
    forecast: ForecastData


def validate_weather_data(current: dict | None) -> WeatherData:
    """Validate that the API returned all fields required by the application.

    Args:
        current: Raw value from the `current` field of the Open-Meteo response.

    Returns:
        A validated weather payload containing the keys used by the application.

    Raises:
        ValueError: If the API does not return the `current` block or if any required
            field is missing.
    """
    if not current:
        raise ValueError("The weather API did not return current conditions.")

    required_fields = (
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m",
        "precipitation",
        "weathercode",
        "time",
    )
    missing_fields = [field for field in required_fields if field not in current]
    if missing_fields:
        missing_fields_text = ", ".join(missing_fields)
        raise ValueError(
            "The weather API returned incomplete data. "
            f"Missing fields: {missing_fields_text}."
        )

    return current  # type: ignore[return-value]


def validate_forecast_data(daily: dict | None) -> ForecastData:
    """Validate that the API returned the daily forecast fields used by the app."""
    if not daily:
        raise ValueError("The weather API did not return a daily forecast.")

    required_fields = ("time", "temperature_2m_max", "temperature_2m_min")
    missing_fields = [field for field in required_fields if field not in daily]
    if missing_fields:
        missing_fields_text = ", ".join(missing_fields)
        raise ValueError(
            "The weather API returned an incomplete daily forecast. "
            f"Missing fields: {missing_fields_text}."
        )

    return daily  # type: ignore[return-value]


def get_weather(lat: float, lon: float, forecast_days: int = 5) -> WeatherBundle:
    """Fetch the current weather and multi-day forecast for a latitude and longitude pair.

    Args:
        lat: Latitude of the selected city.
        lon: Longitude of the selected city.
        forecast_days: Number of days to include in the daily forecast.

    Returns:
        A dictionary with the current weather block and a daily forecast block returned
        by Open-Meteo.

    Raises:
        requests.RequestException: If the HTTP request fails or the API responds with
            a non-success status code.
        ValueError: If the API response does not contain the expected current weather
            payload.

    Example:
        >>> weather = get_weather(-23.55, -46.63)
        >>> weather["current"]["temperature_2m"]
        24.1
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": CURRENT_FIELDS,
        "daily": DAILY_FIELDS,
        "forecast_days": forecast_days,
        "timezone": "auto",
    }

    response = requests.get(FORECAST_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    payload = response.json()
    return {
        "current": validate_weather_data(payload.get("current")),
        "forecast": validate_forecast_data(payload.get("daily")),
    }
