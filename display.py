WEATHER_DESCRIPTIONS = {
    0: "Ceu limpo",
    1: "Predominantemente limpo",
    2: "Parcialmente nublado",
    3: "Encoberto",
    45: "Neblina",
    48: "Neblina com geada",
    51: "Garoa fraca",
    53: "Garoa moderada",
    55: "Garoa intensa",
    61: "Chuva fraca",
    63: "Chuva moderada",
    65: "Chuva forte",
    71: "Neve fraca",
    73: "Neve moderada",
    75: "Neve forte",
    80: "Pancadas de chuva fracas",
    81: "Pancadas de chuva moderadas",
    82: "Pancadas de chuva fortes",
    95: "Trovoadas",
    96: "Trovoadas com granizo fraco",
    99: "Trovoadas com granizo forte",
}


def get_weather_description(code: int | None) -> str:
    if code is None:
        return "Condicao indisponivel"
    return WEATHER_DESCRIPTIONS.get(code, f"Codigo meteorologico {code}")


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
    temperature = current.get("temperature_2m", "N/D")
    humidity = current.get("relative_humidity_2m", "N/D")
    wind_speed = current.get("wind_speed_10m", "N/D")
    precipitation = current.get("precipitation", "N/D")
    updated_at = current.get("time", "N/D")

    print("\n" + "=" * 48)
    print(f"Clima atual - {city}")
    print("=" * 48)
    print(f"Origem dos dados: {source_label}")
    print(f"Temperatura: {temperature} C")
    print(f"Umidade: {humidity} %")
    print(f"Velocidade do vento: {wind_speed} km/h")
    print(f"Precipitacao: {precipitation} mm")
    print(f"Condicao: {description}")
    print(f"Atualizado em: {updated_at}")


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
        ["Data", "Maxima", "Minima"],
        rows,
        f"Previsao para os proximos dias - {city}",
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
        ["Cidade", "Temp.", "Umidade", "Vento", "Precip.", "Condicao", "Origem"],
        rows,
        "Comparacao entre cidades",
    )
