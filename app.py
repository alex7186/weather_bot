#! /usr/bin/python3.10
import os
import time

from back.config_manager import get_config
from back.import_manager import import_modules, execute_modules
from back.text_converter import (
    make_screenpatch_view,
    make_text_from_screenpatch_collection,
    LCDScreen,
)
from back.print_manager import mprint

from modules.base_screen_module import ScreenPatch
from back.i2c_manager import Lcd, CustomCharacters


def get_modules_data(CONFIG):
    """
    importing modules classes from modules '.py' files
    and creating class instances
    """

    # setting up the display
    try:
        display = Lcd()
    except OSError:
        mprint(CONFIG["APP_NAME"] + " " + f": OSError occured")
        exit(1)

    screen = LCDScreen(
        lines_count=CONFIG["LINES_COUNT"], line_length=CONFIG["LINE_LENGTH"]
    )
    custom_charecters = CustomCharacters(display)

    # getting modules configs from './misc/config.json
    modules_list = list(map(lambda x: x["name"], CONFIG["modules_data"]))

    screenpatch_collection = list(
        map(
            lambda x: ScreenPatch(
                rows=x["rows"],
                columns_start=x["columns_start"],
                columns_stop=x["columns_stop"],
            ),
            CONFIG["modules_data"],
        )
    )

    # importing modules
    modules_objects = import_modules(
        modules_list=modules_list,
        CONFIG=CONFIG,
        custom_charecters=custom_charecters,
        screenpatch_collection=screenpatch_collection,
    )

    mprint(CONFIG["APP_NAME"] + " " + f": App started")

    return display, screen, modules_objects, screenpatch_collection


def execute_screen(display, screen, modules_objects, screenpatch_collection):
    """
    executing modules instances and updating the screen
    """
    while True:
        execute_modules(modules_objects=modules_objects)

        unformated_text = make_text_from_screenpatch_collection(
            screen=screen,
            screenpatch_collection=screenpatch_collection,
            modules_objects=modules_objects,
        )

        update_screen(
            display=display,
            unformated_text=unformated_text,
        )

        if CONFIG["PRINT_SCREEN_IMAGE_TO_CONSOLE"]:
            make_screenpatch_view(screen, screenpatch_collection, modules_objects)

        time.sleep(
            CONFIG["GLOBAL_REFRASH_RATE"] - time.time() % CONFIG["GLOBAL_REFRASH_RATE"]
        )


def update_screen(display: Lcd, unformated_text: str) -> None:
    """
    updating the screen with modules text data
    """

    for i_row, line in enumerate(unformated_text):

        display.lcd_display_extended_string(
            line,
            i_row,
        )


if __name__ == "__main__":

    SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-1])
    CONFIG = get_config(SCRIPT_PATH)

    execute_screen(*get_modules_data(CONFIG))
