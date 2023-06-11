from typing import NamedTuple

from back.print_manager import mprint
from modules.base_screen_module import ScreenPatch


class LCDScreen(NamedTuple):
    lines_count: int
    line_length: int


def shift_left(
    text: str, line_length: int = 14, base_margin_left: int = 9, skip_left: int = 0
) -> str:

    return (" " * skip_left + "{:<" + f"{base_margin_left}" + "} ").format(text)


def shift_right(
    text: str, line_length: int = 14, base_margin_left: int = 9, skip_left: int = 0
) -> str:

    text_formatt = (
        " " * skip_left + "{:>" + f"{(line_length - 1)  - base_margin_left}" + "}"
    )
    return (text_formatt).format(text)


def shift_center(
    input_text: str,
    line_length: int = 14,
    base_margin_left: int = 9,
    skip_left: int = 0,
) -> str:

    text = input_text.strip()

    line_clean = text[:]
    while "{" in line_clean:
        bracket_index = line_clean.index("{")
        line_clean = line_clean[:bracket_index] + line_clean[bracket_index + 5 :]
        line_clean = line_clean.replace("}", "@")

    margin = (line_length + 1 - len(line_clean)) // 2
    margin = margin if margin > 0 else 0

    res = (" " * skip_left + "{:>" + f"{margin + len(text)}" + "}").format(text)
    res += " " * (line_length - len(res))

    return res


def make_text_from_screenpatch_collection(
    screen: LCDScreen, screenpatch_collection: list[ScreenPatch], modules_objects
) -> list[str]:

    unformated_text = [" " * screen.line_length] * screen.lines_count

    for i_screenpatch, screenpatch in enumerate(screenpatch_collection):

        screenpatch_text_split = (
            modules_objects[i_screenpatch].get_screenpatch_text().split("\n")
        )

        for row_screenpatch in screenpatch.rows:

            unformated_text[row_screenpatch] = (
                unformated_text[row_screenpatch][: -(screenpatch.columns_start)]
                + screenpatch_text_split[screenpatch.rows.index(row_screenpatch)]
                + unformated_text[row_screenpatch][screenpatch.columns_stop :]
            )

    return unformated_text


def make_screenpatch_view(
    screen: LCDScreen, screenpatch_collection: list[ScreenPatch], modules_objects
) -> None:

    unformated_text = make_text_from_screenpatch_collection(
        screen=screen,
        screenpatch_collection=screenpatch_collection,
        modules_objects=modules_objects,
    )

    s = "\n"
    s += "╭" + (screen.line_length + 1) * "―" + "╮" + "\n"
    for line in unformated_text:
        line_clean = line[:]
        while "{" in line_clean:
            bracket_index = line_clean.index("{")
            line_clean = line_clean[:bracket_index] + line_clean[bracket_index + 5 :]
            line_clean = line_clean.replace("}", "@")
        s += (
            "|"
            + ("{:<" + f"{screen.line_length + 1}" + "}").format(line_clean)
            + "|"
            + "\n"
        )
    s += "╰" + (screen.line_length + 1) * "―" + "╯"
    mprint(s)
