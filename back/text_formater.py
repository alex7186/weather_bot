from typing import NamedTuple

# from back.weather_api_service import Weather
# from modules.base_screen_module import ScreenPatch


class LCDScreen(NamedTuple):
    lines_count: int
    line_length: int


def shift_left(text: str, line_length: int = 14, base_margin_left: int = 9) -> str:

    return ("{:<" + f"{base_margin_left}" + "} ").format(text)


def shift_right(text: str, line_length: int = 14, base_margin_left: int = 9) -> str:

    # print('shift_right', line_length, base_margin_left)
    text_formatt = "{:>" + f"{line_length  - base_margin_left}" + "}"
    # print('text_formatt', text_formatt)
    return (text_formatt).format(text)


def shift_center(
    input_text: str, line_length: int = 14, base_margin_left: int = 9
) -> str:

    text = input_text.strip()

    # print(f'text |{text}| len {len(text)}')
    margin = (line_length + 1 - len(text)) // 2
    margin = margin if margin > 0 else 0
    return ("{:>" + f"{margin + len(text)}" + "}").format(text)


# def brackets(text: str, screenpatch: ScreenPatch) -> str:
#     lines = text.split("\n")

#     if len(lines) > screenpatch.lines_count:
#         raise ValueError("screenpatch size error")

#     s = ""
#     s += "╭" + (screenpatch.line_length + 1) * "―" + "╮" + "\n"

#     for line in lines:
#         s += "|" + ("{:<" + f"{screenpatch.line_length + 1}" + "}").format(line) + "|" + "\n"

#     s += "╰" + (screen.line_length + 1) * "―" + "╯"

#     return s
