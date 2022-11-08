from back.text_converter import LCDScreen

from modules.weather_1line.back.weather_api_service import Weather
from modules.base_screen_module import ScreenPatch

from back.text_converter import shift_center, shift_left, shift_right

base_margin_left = 9


def format_weather(weather: Weather, screenpatch: ScreenPatch) -> str:
    """Formats weather data in string"""

    def format_weather_type(weather: Weather, screenpatch: ScreenPatch):
        def format_temperature(temperature: int) -> str:
            res = "!E"
            if temperature >= 0:
                res = "+" + str(temperature)
            else:
                res = str(temperature)

            return res

        result = ""
        result += " ".join(
            map(
                str,
                (
                    weather.weather_type.value,
                    format_temperature(weather.temperature),
                    "C",
                ),
            )
        )

        return shift_center(
            result.strip(),
            line_length=screenpatch.line_length,
            skip_left=screenpatch.columns_start - 1,
        )

    def format_screen(weather: Weather, screenpatch: ScreenPatch) -> str:

        result = []
        result.append(format_weather_type(weather, screenpatch))

        return "\n".join(result)

    return format_screen(weather, screenpatch)
