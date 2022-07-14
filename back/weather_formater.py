from back.text_formater import LCDScreen

from back.weather_api_service import Weather
from back.text_formater import shift_center, shift_left, shift_right
from modules.base_screen_module import ScreenPatch

base_margin_left = 9


def format_weather(weather: Weather, screenpatch: ScreenPatch) -> str:
    """Formats weather data in string"""

    def format_weather_type(weather: Weather, screenpatch: ScreenPatch):

        result = ""
        result += " ".join(
            map(str, (weather.weather_type.value, weather.temperature, "C"))
        )

        result = shift_center(result.strip(), line_length=screenpatch.line_length)

        return result

    def format_sun_periods(weather: Weather, screenpatch: ScreenPatch) -> str:

        result = ""

        result += f"{weather.sunrise.strftime('%H:%M')}"
        result += " - "
        result += f"{weather.sunset.strftime('%H:%M')}"

        result = shift_center(
            result.strip(),
            line_length=screenpatch.line_length,
        )

        return result

    def format_screen(weather: Weather, screenpatch: ScreenPatch) -> str:

        result = ""
        result += format_weather_type(weather, screenpatch)
        result += "\n"
        result += format_sun_periods(weather, screenpatch)

        result = shift_center(
            result,
            line_length=screenpatch.line_length,
        )

        return result

    return format_screen(weather, screenpatch)
