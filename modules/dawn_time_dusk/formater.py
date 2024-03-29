from datetime import datetime

from back.weather_cache_mananger import Weather, SunPeriods
from back.custom_charecters_manager import (
    CustomCharacters,
    CHARS_SET,
)


base_margin_left = 9


def load_custom_charecters(
    custom_charecters: CustomCharacters, CHARS_SET: dict = CHARS_SET
) -> tuple[str]:
    charecters_address_list = (custom_charecters.append(CHARS_SET["arrow_right"]),)

    custom_charecters.load_custom_characters_data()

    return charecters_address_list


def format_full_screen(
    weather: Weather, sun_periods: SunPeriods, custom_charecters: CustomCharacters
) -> list[str]:

    cur_datetime = datetime.now()

    current_time = (
        cur_datetime.hour if cur_datetime.hour > 9 else "0" + str(cur_datetime.hour),
        cur_datetime.minute
        if cur_datetime.minute > 9
        else "0" + str(cur_datetime.minute),
        cur_datetime.second
        if cur_datetime.second > 9
        else "0" + str(cur_datetime.second),
    )

    result = []

    # if cur_datetime < sun_periods.sunrise:
    # result.append("{}{}:{}:{}".format(custom_charecters[0], *current_time))

    result.append(" {}".format(sun_periods.sunrise.strftime("%H:%M:%S")))

    # if sun_periods.sunrise < cur_datetime < sun_periods.sunset:
    result.append("{}{}:{}:{}".format(custom_charecters[0], *current_time))

    result.append(" {}".format(sun_periods.sunset.strftime("%H:%M:%S")))

    # if sun_periods.sunset < cur_datetime:
    # result.append("{}{}:{}:{}".format(custom_charecters[0], *current_time))

    return "\n".join(result)
