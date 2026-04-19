import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import cache
import config
import logger
import main
import weather


class WeatherAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_artifact_paths = [
            Path("tests") / "weather_log_disabled_test.jsonl",
            Path("tests") / "weather_log_enabled_test.jsonl",
        ]

    def tearDown(self) -> None:
        for path in self.test_artifact_paths:
            if path.exists():
                path.unlink()

    def test_parse_cities_ignores_empty_entries(self) -> None:
        cities = main.parse_cities("Sao Paulo, Rio de Janeiro, , Curitiba  ")
        self.assertEqual(cities, ["Sao Paulo", "Rio de Janeiro", "Curitiba"])

    @patch("builtins.input", return_value="   ")
    def test_main_shows_message_for_empty_input(self, mocked_input) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            main.main()

        self.assertIn("Informe pelo menos uma cidade valida", output.getvalue())
        mocked_input.assert_called_once()

    @patch("main.show_weather")
    @patch("main.show_forecast")
    @patch("main.show_comparison")
    @patch("main.set_cached_weather")
    @patch("main.get_cached_weather", return_value=None)
    @patch("main.log_weather_response")
    @patch(
        "main.get_weather",
        return_value={
            "current": {
                "temperature_2m": 24.1,
                "relative_humidity_2m": 78,
                "wind_speed_10m": 12.3,
                "precipitation": 0.4,
                "weathercode": 2,
                "time": "2026-04-17T21:00",
            },
            "forecast": {
                "time": ["2026-04-18"],
                "temperature_2m_max": [26.0],
                "temperature_2m_min": [18.0],
            },
        },
    )
    @patch("main.get_coordinates", return_value=(-23.55, -46.63))
    def test_process_city_shows_weather_for_valid_city(
        self,
        mocked_get_coordinates,
        mocked_get_weather,
        mocked_log_weather_response,
        mocked_get_cached_weather,
        mocked_set_cached_weather,
        mocked_show_comparison,
        mocked_show_forecast,
        mocked_show_weather,
    ) -> None:
        result = main.process_city("Sao Paulo")

        mocked_get_coordinates.assert_called_once_with("Sao Paulo")
        mocked_get_weather.assert_called_once_with(-23.55, -46.63)
        mocked_get_cached_weather.assert_called_once_with("Sao Paulo")
        mocked_set_cached_weather.assert_called_once()
        mocked_log_weather_response.assert_called_once()
        mocked_show_comparison.assert_not_called()
        mocked_show_forecast.assert_not_called()
        mocked_show_weather.assert_not_called()
        self.assertEqual(result["source"], "API Open-Meteo")

    @patch("main.get_coordinates", side_effect=ValueError("Cidade 'Atlantida' nao encontrada."))
    def test_process_city_reports_city_not_found(self, mocked_get_coordinates) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            main.process_city("Atlantida")

        self.assertIn("Erro em Atlantida", output.getvalue())
        mocked_get_coordinates.assert_called_once_with("Atlantida")

    def test_build_cache_key_normalizes_city_name(self) -> None:
        self.assertEqual(cache.build_cache_key("  Sao Paulo  "), "sao paulo")

    def test_get_cached_weather_returns_none_when_cache_disabled(self) -> None:
        with patch.object(cache, "ENABLE_CACHE", False):
            self.assertIsNone(cache.get_cached_weather("Sao Paulo"))

    def test_log_weather_response_skips_file_when_logging_disabled(self) -> None:
        log_path = Path("tests") / "weather_log_disabled_test.jsonl"
        with patch.object(logger, "ENABLE_LOGGING", False), patch.object(
            logger, "LOG_FILE", log_path
        ):
            logger.log_weather_response("Sao Paulo", {"current": {}})

        self.assertFalse(log_path.exists())

    def test_log_weather_response_writes_file_when_logging_enabled(self) -> None:
        log_path = Path("tests") / "weather_log_enabled_test.jsonl"
        with patch.object(logger, "ENABLE_LOGGING", True), patch.object(
            logger, "LOG_FILE", log_path
        ):
            logger.log_weather_response("Sao Paulo", {"current": {"temperature_2m": 20}})

        content = log_path.read_text(encoding="utf-8").strip()
        payload = json.loads(content)
        self.assertEqual(payload["city"], "Sao Paulo")

    def test_read_bool_env_supports_safe_defaults(self) -> None:
        with patch.dict("os.environ", {"WEATHER_APP_ENABLE_LOGGING": "yes"}, clear=False):
            self.assertTrue(config.read_bool_env("WEATHER_APP_ENABLE_LOGGING", False))

        with patch.dict("os.environ", {"WEATHER_APP_ENABLE_LOGGING": "invalid"}, clear=False):
            self.assertFalse(config.read_bool_env("WEATHER_APP_ENABLE_LOGGING", False))

    def test_validate_weather_data_raises_for_missing_fields(self) -> None:
        incomplete_data = {
            "temperature_2m": 24.1,
            "relative_humidity_2m": 78,
            "precipitation": 0.2,
            "weathercode": 2,
            "time": "2026-04-17T21:00",
        }

        with self.assertRaises(ValueError) as context:
            weather.validate_weather_data(incomplete_data)

        self.assertIn("Campos ausentes", str(context.exception))

    def test_validate_forecast_data_raises_for_missing_fields(self) -> None:
        incomplete_forecast = {
            "time": ["2026-04-18"],
            "temperature_2m_max": [26.0],
        }

        with self.assertRaises(ValueError) as context:
            weather.validate_forecast_data(incomplete_forecast)

        self.assertIn("previsao diaria incompleta", str(context.exception))


if __name__ == "__main__":
    unittest.main()
