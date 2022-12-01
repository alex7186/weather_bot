from typing import Literal, NamedTuple
from typing import NamedTuple
from datetime import datetime
from enum import Enum
import ssl
import requests
from urllib.error import URLError
import json

from modules.weather_1line.back.exceptions import ApiServiceError
from modules.weather_1line.back.coordinates import Coordinates

from back.print_manager import mprint


Celsius = int


class WeatherType(Enum):
    THUNDERSTORM = "Storm"
    DRIZZLE = "Chill"
    RAIN = "Rain"
    SNOW = "Snow"
    CLEAR = "Clear"
    FOG = "Fog"
    CLOUDS = "Clouds"
    NONE = "None"


class Weather(NamedTuple):
    temperature: Celsius = 0
    weather_type: WeatherType = WeatherType.NONE


def get_weather(coordinates: Coordinates, CONFIG: dict) -> Weather:
    """Requests weather in OpenWeather Api and returns it"""

    OPENWEATHER_URL = (
        "https://api.openweathermap.org/data/2.5/"
        + "weather?lat={latitude}&lon={longitude}&units=metric&appid="
        + CONFIG["OPENWEATHER_API_KEY"]
        + "&exclude=daily"
    )

    try:
        openweather_responce = _get_openweather_responce(
            latitude=coordinates.latitude,
            longitude=coordinates.longitude,
            OPENWEATHER_URL=OPENWEATHER_URL,
        )
        weather = _parse_openweather_responce(openweather_responce)

    except Exception:
        mprint(f"Не удалось получить погодные данные по координатам {coordinates}")
        weather = Weather()

    return weather


def _get_openweather_responce(
    latitude: float, longitude: float, OPENWEATHER_URL: str
) -> str:
    ssl.create_default_context = ssl._create_unverified_context
    url = OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)

    try:
        return requests.get(url, timeout=4)

    except URLError:
        raise ApiServiceError


def _parse_openweather_responce(openweather_responce: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_responce.text)
    except json.JSONDecodeError:
        raise ApiServiceError

    temperature = _parse_temperature(openweather_dict)
    weather_type = _parse_weather_type(openweather_dict)

    return Weather(
        temperature=temperature,
        weather_type=weather_type,
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict["main"]["temp"])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])

    except (IndexError, KeyError):
        raise ApiServiceError

    weather_types = {
        "2": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "741": WeatherType.FOG,
        "701": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS,
    }

    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type

    raise ApiServiceError(f"illegal {weather_type_id=}")
