from back.cache_mananger import SunPeriods
from back.text_converter import shift_center
from back.custom_charecters_manager import (
    CustomCharacters,
    CHARS_SET,
    v_invert,
    h_invert,
)

from modules.base_screen_module import ScreenPatch


base_margin_left = 9


def load_custom_charecters(
    custom_charecters: CustomCharacters, CHARS_SET: dict = CHARS_SET
) -> tuple:
    charecters_address_list = (
        custom_charecters.append(CHARS_SET["sun_top_l"]),
        custom_charecters.append(h_invert(CHARS_SET["sun_top_l"])),
        custom_charecters.append(v_invert(CHARS_SET["sun_top_l"])),
        custom_charecters.append(h_invert(v_invert(CHARS_SET["sun_top_l"]))),
    )

    custom_charecters.load_custom_characters_data()

    return charecters_address_list


def format_sun(
    sun_periods: SunPeriods,
    screenpatch: ScreenPatch,
    charecters_address_list: list,
) -> str:
    """Formats sun periods data in string"""

    result = (
        shift_center(
            charecters_address_list[0]
            + charecters_address_list[1]
            + " "
            + sun_periods.sunset.strftime("%H:%M"),
            line_length=screenpatch.line_length,
        ),
        shift_center(
            charecters_address_list[2]
            + charecters_address_list[3]
            + " "
            + sun_periods.sunrise.strftime("%H:%M"),
            line_length=screenpatch.line_length,
        ),
    )

    return "\n".join(result)
