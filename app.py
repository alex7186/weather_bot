#! /usr/bin/python3.10
import os
import time

from back.config_manager import get_config
from back.import_manager import import_modules, execute_modules
from back.text_formater import (
    make_screenpatch_view,
    make_text_from_screenpatch_collection,
)

from modules.base_screen_module import ScreenPatch
from back.text_formater import LCDScreen
from back.lcd.drivers import Lcd, CustomCharacters


def setup(CONFIG):
    """
    importing modules classes from modules '.py' files
    and creating class instances
    """
    imported_modules = []

    # setting up the display
    display = Lcd()
    display.lcd_clear()
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

    return display, screen, modules_objects, screenpatch_collection


def main(display, screen, modules_objects, screenpatch_collection):
    """
    executing modules instances and updating the screen
    """
    while True:
        modules_res = execute_modules(modules_objects)

        # for module_res in modules_res:

        #     if not len(module_res):
        #         continue

        #     module_output_arguments = list(module_res)[0].result()

        update_screen(
            display=display,
            modules_objects=modules_objects,
            # screenpatch=module_output_arguments["screenpatch"],
        )

        if CONFIG["PRINT_SCREEN_IMAGE_TO_CONSOLE"]:
            make_screenpatch_view(screen, screenpatch_collection, modules_objects)

        time.sleep(
            CONFIG["GLOBAL_REFRASH_RATE"] - time.time() % CONFIG["GLOBAL_REFRASH_RATE"]
        )


def update_screen(display: Lcd, modules_objects) -> None:
    """
    updating the screen with modules text data
    """

    unformated_text = make_text_from_screenpatch_collection(
        screen=screen,
        screenpatch_collection=screenpatch_collection,
        modules_objects=modules_objects,
    )

    for i_row, line in enumerate(unformated_text):
        display.lcd_display_string(
            line,
            i_row + 1,
        )


if __name__ == "__main__":

    SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-1])
    CONFIG = get_config(SCRIPT_PATH)

    display, screen, modules_objects, screenpatch_collection = setup(CONFIG)
    main(display, screen, modules_objects, screenpatch_collection)
