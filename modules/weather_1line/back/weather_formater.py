from back.weather_cache_mananger import Weather
from back.custom_charecters_manager import CustomCharacters, CHARS_SET

from modules.base_screen_module import ScreenPatch


base_margin_left = 9


def load_custom_charecters(
    custom_charecters: CustomCharacters, CHARS_SET: dict = CHARS_SET
) -> tuple:
    charecters_address_list = (custom_charecters.append(CHARS_SET["degree"]),)
    custom_charecters.load_custom_characters_data()

    return charecters_address_list


def format_weather(
    weather: Weather,
    screenpatch: ScreenPatch,
    charecters_address_list: list,
) -> str:
    """Formats weather data in string"""

    def format_temperature(temperature: int) -> str:
        res = "!E"
        if temperature >= 0:
            res = "+" + str(temperature)
        else:
            res = str(temperature)
        return res

    temperature = (
        format_temperature(weather.temperature) + " C" + charecters_address_list[0]
    )

    result = "  {:6} ||  {}".format(weather.weather_type.value, temperature)

    return result
