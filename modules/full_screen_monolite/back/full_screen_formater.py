# format_full_screen
# load_custom_charecters
from datetime import datetime

from back.print_manager import mprint

# from back.cache_mananger import Weather, SunPeriods
from back.custom_charecters_manager import (
    CustomCharacters,
    CHARS_SET,
    v_invert,
    h_invert,
)

# from modules.base_screen_module import ScreenPatch


base_margin_left = 9


def load_custom_charecters(
    custom_charecters: CustomCharacters, CHARS_SET: dict = CHARS_SET
) -> tuple:
    charecters_address_list = (
        custom_charecters.append(CHARS_SET["sun_top_l"]),
        custom_charecters.append(h_invert(CHARS_SET["sun_top_l"])),
        custom_charecters.append(v_invert(CHARS_SET["sun_top_l"])),
        custom_charecters.append(h_invert(v_invert(CHARS_SET["sun_top_l"]))),
        custom_charecters.append(CHARS_SET["degree"]),
        custom_charecters.append(CHARS_SET["arrow_both"]),
        custom_charecters.append(CHARS_SET["sun_1"]),
    )

    custom_charecters.load_custom_characters_data()

    return charecters_address_list


def format_full_screen(weather, sun_periods, screenpatch, custom_charecters):
    def format_temperature(temperature: int) -> str:
        res = "!E"
        if temperature >= 0:
            res = "+" + str(temperature)
        else:
            res = str(temperature)
        return res

    cur_datetime = datetime.now()
    cur_hour = cur_datetime.hour
    cur_minute = cur_datetime.minute
    cur_second = cur_datetime.second

    arr = (
        cur_hour if cur_hour > 9 else "0" + str(cur_hour),
        cur_minute if cur_minute > 9 else "0" + str(cur_minute),
        cur_second if cur_second > 9 else "0" + str(cur_second),
        weather.weather_type.value,
        cur_datetime.day if cur_datetime.day > 9 else "0" + str(cur_datetime.day),
        cur_datetime.month if cur_datetime.month > 9 else "0" + str(cur_datetime.month),
        str(cur_datetime.year)[2:],
        format_temperature(weather.temperature) + " C" + custom_charecters[4],
        sun_periods.sunset.strftime("%H:%M"),
        sun_periods.sunrise.strftime("%H:%M"),
    )

    result = [
        "  {}:{}:{}   {:6} ".format(*arr[:4]),
        "  {}.{}.{}   {}".format(*arr[4:8]),
        "  {} {}".format(custom_charecters[5], arr[8]),
        "  {} {}".format(custom_charecters[6], arr[9]),
    ]

    return "\n".join(result)
