WEATHER_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with light hail",
    99: "Thunderstorm with heavy hail",
}


def get_weather_description(code: int | None) -> str:
    if code is None:
        return "Condition unavailable"
    return WEATHER_DESCRIPTIONS.get(code, f"Weather code {code}")


def _format_row(columns: list[str], widths: list[int]) -> str:
    padded_columns = [value.ljust(width) for value, width in zip(columns, widths)]
    return "| " + " | ".join(padded_columns) + " |"


def _print_table(headers: list[str], rows: list[list[str]], title: str) -> None:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    separator = "+-" + "-+-".join("-" * width for width in widths) + "-+"

    print(f"\n{title}")
    print(separator)
    print(_format_row(headers, widths))
    print(separator)
    for row in rows:
        print(_format_row(row, widths))
    print(separator)


def show_weather(city: str, weather_bundle: dict, source_label: str) -> None:
    current = weather_bundle["current"]
    description = get_weather_description(current.get("weathercode"))
    temperature = current.get("temperature_2m", "N/A")
    humidity = current.get("relative_humidity_2m", "N/A")
    wind_speed = current.get("wind_speed_10m", "N/A")
    precipitation = current.get("precipitation", "N/A")
    updated_at = current.get("time", "N/A")

    print("\n" + "=" * 48)
    print(f"Current weather - {city}")
    print("=" * 48)
    print(f"Data source: {source_label}")
    print(f"Temperature: {temperature} C")
    print(f"Humidity: {humidity} %")
    print(f"Wind speed: {wind_speed} km/h")
    print(f"Precipitation: {precipitation} mm")
    print(f"Condition: {description}")
    print(f"Updated at: {updated_at}")


def show_forecast(city: str, weather_bundle: dict) -> None:
    forecast = weather_bundle["forecast"]
    rows = []

    for date, max_temp, min_temp in zip(
        forecast["time"],
        forecast["temperature_2m_max"],
        forecast["temperature_2m_min"],
    ):
        rows.append([date, f"{max_temp} C", f"{min_temp} C"])

    _print_table(
        ["Date", "High", "Low"],
        rows,
        f"Forecast for the next few days - {city}",
    )


def show_comparison(results: list[dict]) -> None:
    rows = []

    for result in results:
        current = result["weather"]["current"]
        rows.append(
            [
                result["city"],
                f"{current['temperature_2m']} C",
                f"{current['relative_humidity_2m']} %",
                f"{current['wind_speed_10m']} km/h",
                f"{current['precipitation']} mm",
                get_weather_description(current["weathercode"]),
                result["source"],
            ]
        )

    _print_table(
        ["City", "Temp.", "Humidity", "Wind", "Precip.", "Condition", "Source"],
        rows,
        "City comparison",
    )
