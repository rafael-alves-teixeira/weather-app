import os


TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}


def read_bool_env(name: str, default: bool) -> bool:
    """Read a boolean environment variable with a safe fallback."""
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    normalized = raw_value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    return default


ENABLE_CACHE = read_bool_env("WEATHER_APP_ENABLE_CACHE", True)
ENABLE_LOGGING = read_bool_env("WEATHER_APP_ENABLE_LOGGING", False)
