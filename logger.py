import json
from datetime import datetime
from pathlib import Path

from config import ENABLE_LOGGING

LOG_FILE = Path("weather_log.jsonl")


def log_weather_response(city: str, data: dict) -> None:
    """Append a successful weather lookup to the local JSON Lines log file.

    Args:
        city: Name of the city used in the query.
        data: Weather data returned by the API for the city.
    """
    if not ENABLE_LOGGING:
        return

    entry = {
        "logged_at": datetime.now().isoformat(timespec="seconds"),
        "city": city,
        "data": data,
    }
    with LOG_FILE.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(entry, ensure_ascii=True) + "\n")
