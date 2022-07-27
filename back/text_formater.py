from typing import NamedTuple


class LCDScreen(NamedTuple):
    lines_count: int
    line_length: int


def shift_left(text: str, line_length: int = 14, base_margin_left: int = 9) -> str:

    return ("{:<" + f"{base_margin_left}" + "} ").format(text)


def shift_right(text: str, line_length: int = 14, base_margin_left: int = 9) -> str:

    text_formatt = "{:>" + f"{line_length  - base_margin_left}" + "}"
    return (text_formatt).format(text)


def shift_center(
    input_text: str, line_length: int = 14, base_margin_left: int = 9
) -> str:

    text = input_text.strip()

    margin = (line_length + 1 - len(text)) // 2
    margin = margin if margin > 0 else 0

    res = ("{:>" + f"{margin + len(text)}" + "}").format(text)
    res += " " * (line_length - len(res))

    return res


def make_text_from_screenpatch_collection(
    screen: LCDScreen, screenpatch_collection: list, modules_objects
) -> str:
    unformated_text = [""] * screen.lines_count

    for i_screenpatch, screenpatch in enumerate(screenpatch_collection):
        screenpatch_text_split = (
            modules_objects[i_screenpatch].get_screenpatch_text().split("\n")
        )

        for i_row, row_screenpatch in enumerate(screenpatch.rows):
            print(i_row, screenpatch_text_split)
            unformated_text[row_screenpatch] = screenpatch_text_split[i_row]

    return unformated_text


def make_screenpatch_view(
    screen: LCDScreen, screenpatch_collection: list, modules_objects
):

    unformated_text = make_text_from_screenpatch_collection(
        screen=screen,
        screenpatch_collection=screenpatch_collection,
        modules_objects=modules_objects,
    )

    s = ""
    s += "╭" + (screen.line_length + 1) * "―" + "╮" + "\n"
    for line in unformated_text:
        s += "|" + ("{:<" + f"{screen.line_length + 1}" + "}").format(line) + "|" + "\n"
    s += "╰" + (screen.line_length + 1) * "―" + "╯"
    print(s)
