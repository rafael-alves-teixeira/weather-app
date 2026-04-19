import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
REQUEST_TIMEOUT = 10


def get_coordinates(city: str) -> tuple[float, float]:
    """Look up the latitude and longitude for a city name.

    Args:
        city: Name of the city entered by the user.

    Returns:
        A tuple containing latitude and longitude for the first search result.

    Raises:
        requests.RequestException: If the geocoding request fails.
        ValueError: If the city is empty in practice or no matching result is found.

    Example:
        >>> get_coordinates("Sao Paulo")
        (-23.5505, -46.6333)
    """
    response = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1, "language": "en"},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    results = response.json().get("results")
    if not results:
        raise ValueError(f"City '{city}' was not found.")

    return results[0]["latitude"], results[0]["longitude"]
