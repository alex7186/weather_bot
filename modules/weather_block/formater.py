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
    )

    custom_charecters.load_custom_characters_data()

    return charecters_address_list


def format_full_screen(
    weather: Weather, sun_periods: SunPeriods, custom_charecters: CustomCharacters
) -> list[str]:
    def format_temperature(temperature: Celsius) -> str:

        return (
            "" + "-"
            if temperature < 0
            else "+" + ("0" if abs(temperature) < 10 else "") + str(temperature)
        )

    cur_datetime = datetime.now()

    current_date = (
        cur_datetime.day if cur_datetime.day > 9 else "0" + str(cur_datetime.day),
        cur_datetime.month if cur_datetime.month > 9 else "0" + str(cur_datetime.month),
        str(cur_datetime.year)[2:],
    )

    result = []

    result.append(" {}/{}/{}".format(*current_date))
    result.append(
        " {:<8}".format(
            format_temperature(weather.temperature) + " C" + custom_charecters[0]
        )
    )
    result.append(" {:<8}".format(weather.weather_type.value))
    result.append(" {:<8}".format(calendar.day_name[cur_datetime.weekday()][:3]))

    return "\n".join(result)
