#! /usr/bin/python3.10
import os

from back.config_manager import get_config
from back.coordinates import Coordinates
from back.text_formater import LCDScreen

from back.lcd.drivers import Lcd

from modules.base_screen_module import ScreenPatch
from back.import_manager import import_modules, start_modules, execute_modules


screen: LCDScreen
display: Lcd
coordinates: Coordinates


SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-1])
CONFIG = get_config(SCRIPT_PATH)


imported_modules: list = []


def setup():
    global screen
    global coordinates
    global display

    global imported_modules

    screen = LCDScreen(
        lines_count=CONFIG["LINES_COUNT"], line_length=CONFIG["LINE_LENGTH"]
    )

    display = Lcd()

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

    # importing ScreenPatch modules
    imported_modules = import_modules(modules_list=modules_list)

    # executing the `setup` method of every module
    tasks_group = start_modules(
        imported_modules=imported_modules,
        screenpatch_collection=screenpatch_collection,
        display=display,
        CONFIG=CONFIG,
    )
    display.lcd_clear()


def main():
    global screen
    global CONFIG

    global imported_modules

    execute_modules(imported_modules=imported_modules)


if __name__ == "__main__":
    setup()
    main()
