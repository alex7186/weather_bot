import json
from back.text_converter import LCDScreen

from modules.sun_2line.back.weather_api_service import SunPeriods
from modules.base_screen_module import ScreenPatch

from back.text_converter import shift_center, shift_left, shift_right
from back.i2c_dev import CustomCharacters
from back.custom_charecters_manager import reflect_hor, reflect_vert

base_margin_left = 9


def format_sun(
    sun_periods: SunPeriods,
    screenpatch: ScreenPatch,
    custom_charecters: CustomCharacters,
) -> str:
    """Formats weather data in string"""

    result = []

    # with open(f"misc/custom_chars.json", "r") as f:
    #     sun_top_l = json.load(f)["sun_top_l"]

    # sun_custom_charecters = {
    #     "sun_top_l": sun_top_l,
    #     "sun_top_r": reflect_hor(sun_top_l),
    #     "sun_btm_l": reflect_vert(sun_top_l),
    #     "sun_btm_r": reflect_hor(reflect_vert(sun_top_l)),
    # }

    with open(f"misc/custom_chars.json", "r") as f:
        res = json.load(f)

        arrow_top_l = res["arrow_top_l"]
        arrow_btm_l = res["arrow_btm_l"]

    sun_custom_charecters = {
        "sun_top_l": arrow_top_l,
        "sun_top_r": reflect_hor(arrow_top_l),
        "sun_btm_l": arrow_btm_l,
        "sun_btm_r": reflect_hor(arrow_btm_l),
    }

    custom_charecters.char_1_data = sun_custom_charecters["sun_top_l"]
    custom_charecters.char_2_data = sun_custom_charecters["sun_top_r"]
    custom_charecters.char_3_data = sun_custom_charecters["sun_btm_l"]
    custom_charecters.char_4_data = sun_custom_charecters["sun_btm_r"]

    custom_charecters.load_custom_characters_data()

    ccd = {
        "sun_top_l": "{0x00}",
        "sun_top_r": "{0x01}",
        "sun_btm_l": "{0x02}",
        "sun_btm_r": "{0x03}",
    }

    result.append(
        shift_center(
            f"{ccd['sun_top_l']}{ccd['sun_top_r']} {sun_periods.sunset.strftime('%H:%M')}",
            line_length=screenpatch.line_length,
        )
    )
    result.append(
        shift_center(
            f"{ccd['sun_btm_l']}{ccd['sun_btm_r']} {sun_periods.sunrise.strftime('%H:%M')}",
            line_length=screenpatch.line_length,
        )
    )

    return "\n".join(result)
