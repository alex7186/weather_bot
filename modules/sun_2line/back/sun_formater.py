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


def format_sun(
    sun_periods: SunPeriods,
    screenpatch: ScreenPatch,
    custom_charecters: CustomCharacters,
) -> str:
    """Formats sun periods data in string"""

    sun_1 = custom_charecters.append(CHARS_SET["sun_top_l"])
    sun_2 = custom_charecters.append(h_invert(CHARS_SET["sun_top_l"]))
    sun_3 = custom_charecters.append(v_invert(CHARS_SET["sun_top_l"]))
    sun_4 = custom_charecters.append(h_invert(v_invert(CHARS_SET["sun_top_l"])))
    custom_charecters.load_custom_characters_data()

    result = (
        shift_center(
            sun_1 + sun_2 + " " + sun_periods.sunset.strftime("%H:%M"),
            line_length=screenpatch.line_length,
        ),
        shift_center(
            sun_3 + sun_4 + " " + sun_periods.sunrise.strftime("%H:%M"),
            line_length=screenpatch.line_length,
        ),
    )

    return "\n".join(result)
