from typing import NamedTuple
from enum import Enum
import ssl
import requests
from urllib.error import URLError
import json
import pickle
from datetime import datetime, timedelta

from back.coords_manager import Coordinates
from back.print_manager import mprint


Celsius = int


class ApiServiceError(Exception):
    """Program can't connect to API"""

    pass


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


class SunPeriods(NamedTuple):
    sunrise: datetime = datetime(year=1970, month=1, day=1, hour=0, minute=0)
    sunset: datetime = datetime(year=1970, month=1, day=1, hour=0, minute=0)


def get_weather(coordinates: Coordinates, CONFIG: dict):
    """Requests weather in OpenWeather Api and returns it"""

    def update_cache(data):
        with open("misc/weather_cache.txt", "wb") as file:
            current_time = datetime.now()
            pickle.dump((current_time, data), file)
            print(f"dumping {data} at {current_time}")

    def read_cache():
        with open("misc/weather_cache.txt", "rb") as file:
            return pickle.load(file)

    OPENWEATHER_URL = (
        "https://api.openweathermap.org/data/2.5/"
        + "weather?lat={latitude}&lon={longitude}"
        + "&units=metric&appid="
        + CONFIG["OPENWEATHER_API_KEY"]
        + "&exclude=daily"
    )

    cache = read_cache()

    current_time = datetime.now()
    cached_time = cache[0]
    cached_data = cache[1]

    if current_time - cached_time > timedelta(hours=3):
        try:
            openweather_responce = _get_openweather_responce(
                latitude=coordinates.latitude,
                longitude=coordinates.longitude,
                OPENWEATHER_URL=OPENWEATHER_URL,
            )
            data = _parse_openweather_responce(openweather_responce)
            result = (
                Weather(
                    temperature=data["temperature"],
                    weather_type=data["weather_type"],
                ),
                SunPeriods(
                    sunset=data["sunset"],
                    sunrise=data["sunrise"],
                ),
            )
            update_cache(result)

            return result

        except ApiServiceError:
            mprint(f"Не удалось получить погодные данные по координатам {coordinates}")
            return cached_data

    else:
        return cached_data


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
    def _parse_suntime(openweather_dict: dict, time) -> datetime:
        return datetime.fromtimestamp(openweather_dict["sys"][time])

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

    try:
        openweather_dict = json.loads(openweather_responce.text)
    except json.JSONDecodeError:
        raise ApiServiceError

    temperature = _parse_temperature(openweather_dict)
    weather_type = _parse_weather_type(openweather_dict)
    sunset = _parse_suntime(openweather_dict, "sunset")
    sunrise = _parse_suntime(openweather_dict, "sunrise")

    return {
        "temperature": temperature,
        "weather_type": weather_type,
        "sunset": sunset,
        "sunrise": sunrise,
    }
