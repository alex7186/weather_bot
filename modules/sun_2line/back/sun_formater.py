import json
from back.text_converter import LCDScreen

from modules.sun_2line.back.weather_api_service import SunPeriods
from modules.base_screen_module import ScreenPatch

from back.text_converter import shift_center, shift_left, shift_right
from back.i2c_manager import CustomCharacters
from back.custom_charecters_manager import reflect_hor, reflect_vert

base_margin_left = 9


def format_sun(
    sun_periods: SunPeriods,
    screenpatch: ScreenPatch,
    custom_charecters: CustomCharacters,
) -> str:
    """Formats weather data in string"""

    with open(f"misc/custom_chars.json", "r") as f:
        res = json.load(f)

        # arrow_top_l = res["arrow_top_l"]
        # arrow_btm_l = res["arrow_btm_l"]
        arrow_up = res["arrow_up"]
        sun_1 = res["sun_1"]

    # sun_custom_charecters = {
    #     "sun_top_l": arrow_top_l,
    #     "sun_top_r": reflect_hor(arrow_top_l),
    #     "sun_btm_l": arrow_btm_l,
    #     "sun_btm_r": reflect_hor(arrow_btm_l),
    # }

    sun_custom_charecters = {"arrow_up": arrow_up, "sun_1": sun_1}

    for i, custom_char in enumerate(sun_custom_charecters.values()):
        custom_charecters.chars_list[i] = custom_char

    custom_charecters.load_custom_characters_data()

    # custom_charecters_adresses = {
    #     "sun_top_l": "{0x00}",
    #     "sun_top_r": "{0x01}",
    #     "sun_btm_l": "{0x02}",
    #     "sun_btm_r": "{0x03}",
    # }

    custom_charecters_adresses = {"arrow_up": "{0x00}", "sun_1": "{0x01}"}

    result = []

    result.append(
        shift_center(
            # f"{custom_charecters_adresses['sun_top_l']}"
            # + f"{custom_charecters_adresses['sun_top_r']}"
            f'{custom_charecters_adresses["arrow_up"]}'
            + " "
            + f"{sun_periods.sunset.strftime('%H:%M')}",
            line_length=screenpatch.line_length,
        )
    )
    result.append(
        shift_center(
            # f"{custom_charecters_adresses['sun_btm_l']}"
            # + f"{custom_charecters_adresses['sun_btm_r']}"
            f'{custom_charecters_adresses["sun_1"]}'
            + " "
            + f"{sun_periods.sunrise.strftime('%H:%M')}",
            line_length=screenpatch.line_length,
        )
    )

    return "\n".join(result)
