import requests

from cache import get_cached_weather, set_cached_weather
from display import show_weather
from display import show_comparison
from display import show_forecast
from geocoding import get_coordinates
from logger import log_weather_response
from weather import get_weather


def parse_cities(raw_value: str) -> list[str]:
    """Split a comma-separated input string into normalized city names."""
    cities = [city.strip() for city in raw_value.split(",")]
    return [city for city in cities if city]


def process_city(city: str) -> dict | None:
    """Fetch, cache, log and display the weather for a single city."""
    cached_weather = get_cached_weather(city)
    if cached_weather:
        log_weather_response(city, cached_weather)
        return {"city": city, "weather": cached_weather, "source": "cache local"}

    try:
        lat, lon = get_coordinates(city)
        data = get_weather(lat, lon)
    except ValueError as error:
        print(f"Erro em {city}: {error}")
        return
    except requests.RequestException:
        print(f"Erro em {city}: nao foi possivel consultar a API no momento.")
        return None

    set_cached_weather(city, data)
    log_weather_response(city, data)
    return {"city": city, "weather": data, "source": "API Open-Meteo"}


def main() -> None:
    """Run the command-line workflow for one or more cities."""
    raw_cities = input("Digite uma ou mais cidades separadas por virgula: ").strip()
    cities = parse_cities(raw_cities)
    if not cities:
        print("Informe pelo menos uma cidade valida para realizar a consulta.")
        return

    results = []
    for city in cities:
        result = process_city(city)
        if result:
            results.append(result)

    if not results:
        print("Nenhuma consulta foi concluida com sucesso.")
        return

    show_comparison(results)

    for result in results:
        show_weather(result["city"], result["weather"], result["source"])
        show_forecast(result["city"], result["weather"])


if __name__ == "__main__":
    main()
