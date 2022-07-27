from datetime import datetime

from back.weather_formater import LCDScreen
from back.text_formater import shift_left, shift_right


def get_date_string(screen: LCDScreen) -> str:
    cur_datetime = datetime.now()
    cur_hour = cur_datetime.hour
    cur_minute = cur_datetime.minute
    # cur_second = cur_datetime.second

    s = ""
    s += shift_left(
        "{}.{}.{}".format(cur_datetime.year, cur_datetime.month, cur_datetime.day),
        line_length=screen.line_length,
    )

    s += shift_right(
        "{}:{}".format(
            cur_hour if cur_hour > 9 else "0" + str(cur_hour),
            cur_minute if cur_minute > 9 else "0" + str(cur_minute),
            # cur_second if cur_second > 9 else '0' + str(cur_second)
        ),
        line_length=screen.line_length,
    )

    return s
