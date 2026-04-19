import json
from datetime import datetime, timedelta
from pathlib import Path

from config import ENABLE_CACHE

CACHE_FILE = Path("weather_cache.json")
CACHE_TTL = timedelta(hours=1)


def _load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}

    with CACHE_FILE.open("r", encoding="utf-8") as cache_file:
        try:
            return json.load(cache_file)
        except json.JSONDecodeError:
            return {}


def _save_cache(cache_data: dict) -> None:
    with CACHE_FILE.open("w", encoding="utf-8") as cache_file:
        json.dump(cache_data, cache_file, ensure_ascii=True, indent=2)


def build_cache_key(city: str) -> str:
    return city.strip().lower()


def get_cached_weather(city: str) -> dict | None:
    if not ENABLE_CACHE:
        return None

    cache_data = _load_cache()
    cache_key = build_cache_key(city)
    cached_entry = cache_data.get(cache_key)
    if not cached_entry:
        return None

    cached_at_raw = cached_entry.get("cached_at")
    if not cached_at_raw:
        return None

    cached_at = datetime.fromisoformat(cached_at_raw)
    if datetime.now() - cached_at > CACHE_TTL:
        return None

    return cached_entry.get("payload")


def set_cached_weather(city: str, payload: dict) -> None:
    if not ENABLE_CACHE:
        return

    cache_data = _load_cache()
    cache_key = build_cache_key(city)
    cache_data[cache_key] = {
        "city": city,
        "cached_at": datetime.now().isoformat(timespec="seconds"),
        "payload": payload,
    }
    _save_cache(cache_data)
