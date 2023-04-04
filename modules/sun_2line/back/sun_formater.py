import json

from back.cache_mananger import SunPeriods
from back.text_converter import shift_center
from back.i2c_manager import CustomCharacters
from back.custom_charecters_manager import reflect_vert, reflect_hor

from modules.base_screen_module import ScreenPatch


base_margin_left = 9


def format_sun(
    sun_periods: SunPeriods,
    screenpatch: ScreenPatch,
    custom_charecters: CustomCharacters,
) -> str:
    """Formats weather data in string"""

    with open(f"misc/custom_chars.json", "r") as f:
        chars = json.load(f)

    symbols_adress_list = [
        # custom_charecters.append(chars["arrow_up"]),
        # custom_charecters.append(reflect_vert(chars["arrow_up"])),
        # custom_charecters.append(chars["sun_1"]),
        custom_charecters.append(chars["sun_top_l"]),
        custom_charecters.append(reflect_hor(chars["sun_top_l"])),
        custom_charecters.append(reflect_vert(chars["sun_top_l"])),
        custom_charecters.append(reflect_hor(reflect_vert(chars["sun_top_l"]))),
    ]

    custom_charecters.load_custom_characters_data()

    result = (
        shift_center(
            symbols_adress_list[0]
            + symbols_adress_list[1]
            + f" {sun_periods.sunset.strftime('%H:%M')}",
            line_length=screenpatch.line_length,
        ),
        shift_center(
            symbols_adress_list[2]
            + symbols_adress_list[3]
            + f" {sun_periods.sunrise.strftime('%H:%M')}",
            line_length=screenpatch.line_length,
        ),
    )

    return "\n".join(result)
