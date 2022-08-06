from typing import Literal, NamedTuple
from typing import NamedTuple
from datetime import datetime
from enum import Enum
import ssl
import requests
from urllib.error import URLError
import json

from modules.sun_2line.back.exceptions import ApiServiceError
from modules.sun_2line.back.coordinates import Coordinates


class SunPeriods(NamedTuple):
    sunrise: datetime = datetime.now()
    sunset: datetime = datetime.now()


def get_sun(coords: Coordinates, CONFIG: dict) -> SunPeriods:
    """Requests weather in OpenWeather Api and returns it"""

    OPENWEATHER_URL = (
        "https://api.openweathermap.org/data/2.5/"
        + "weather?lat={latitude}&lon={longitude}&units=metric&appid="
        + CONFIG["OPENWEATHER_API_KEY"]
        + "&exclude=daily"
    )

    try:
        openweather_responce = _get_openweather_responce(
            latitude=coords.latitude,
            longitude=coords.longitude,
            OPENWEATHER_URL=OPENWEATHER_URL,
        )
        weather = _parse_openweather_responce(openweather_responce)
        return weather
    except Exception:
        raise ApiServiceError(f"Не удалось получить погоду по координатам {coords}")


def _get_openweather_responce(
    latitude: float, longitude: float, OPENWEATHER_URL: str
) -> str:
    ssl.create_default_context = ssl._create_unverified_context
    url = OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)

    try:
        return requests.get(url)

    except URLError:
        raise ApiServiceError


def _parse_openweather_responce(openweather_responce: str) -> SunPeriods:
    def _parse_suntime(
        openweather_dict: dict, time  #: Literal["sunrise"] | Literal["sunset"]
    ) -> datetime:
        return datetime.fromtimestamp(openweather_dict["sys"][time])

    try:
        openweather_dict = json.loads(openweather_responce.text)
    except json.JSONDecodeError:
        raise ApiServiceError

    sunset = _parse_suntime(openweather_dict, "sunset")
    sunrise = _parse_suntime(openweather_dict, "sunrise")

    return SunPeriods(
        sunset=sunset,
        sunrise=sunrise,
    )
