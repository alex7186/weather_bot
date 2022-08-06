from back.text_formater import LCDScreen

from modules.sun_2line.back.weather_api_service import SunPeriods
from modules.base_screen_module import ScreenPatch

from back.text_formater import shift_center, shift_left, shift_right

base_margin_left = 9


def format_sun(sun_periods: SunPeriods, screenpatch: ScreenPatch) -> str:
    """Formats weather data in string"""

    result = []

    ccd = {
        "sun_top_l": "A",
        "sun_top_r": "a",
        "sun_btm_l": "B",
        "sun_btm_r": "b",
    }

    result.append(
        shift_left(
            f"{ccd['sun_top_l']}{ccd['sun_top_r']} {sun_periods.sunset.strftime('%H:%M')}",
            line_length=screenpatch.line_length,
        )
    )
    result.append(
        shift_left(
            f"{ccd['sun_btm_l']}{ccd['sun_btm_r']} {sun_periods.sunrise.strftime('%H:%M')}",
            line_length=screenpatch.line_length,
        )
    )

    return "\n".join(result)
