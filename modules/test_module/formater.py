from datetime import datetime
import calendar

from back.weather_cache_mananger import Weather, SunPeriods, Celsius
from back.custom_charecters_manager import (
    CustomCharacters,
    CHARS_SET,
    v_invert,
    h_invert,
)


base_margin_left = 9


def load_custom_charecters(
    custom_charecters: CustomCharacters, CHARS_SET: dict = CHARS_SET
) -> tuple[str]:
    charecters_address_list = (
        custom_charecters.append(CHARS_SET["degree"]),
        custom_charecters.append(CHARS_SET["arrow_right"]),
        custom_charecters.append(CHARS_SET["arrow_simple_right"]),
    )

    custom_charecters.load_custom_characters_data()

    return charecters_address_list
