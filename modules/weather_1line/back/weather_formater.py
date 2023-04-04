from back.cache_mananger import Weather
from back.text_converter import shift_center
from back.custom_charecters_manager import CustomCharacters, CHARS_SET

from modules.base_screen_module import ScreenPatch


base_margin_left = 9


def format_weather(
    weather: Weather,
    screenpatch: ScreenPatch,
    custom_charecters: CustomCharacters,
) -> str:
    """Formats weather data in string"""

    def format_temperature(temperature: int) -> str:
        res = "!E"
        if temperature >= 0:
            res = "+" + str(temperature)
        else:
            res = str(temperature)
        return res

    degree_celsium_symbol = custom_charecters.append(CHARS_SET["degree"])
    custom_charecters.load_custom_characters_data()

    result = (
        shift_center(
            weather.weather_type.value
            + " "
            + format_temperature(weather.temperature)
            + " C"
            + degree_celsium_symbol,
            line_length=screenpatch.line_length,
            skip_left=screenpatch.columns_start - 1,
        ),
    )

    return "\n".join(result)
