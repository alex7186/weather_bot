#! /usr/bin/python3.10
import os
import asyncio
import time


from back.config_manager import get_config

from back.text_formater import LCDScreen

from back.lcd.drivers import Lcd

from modules.base_screen_module import ScreenPatch
from back.import_manager import import_modules, setup_modules
from back.text_formater import (
    shift_center,
    make_screenpatch_view,
    make_text_from_screenpatch_collection,
)


def update_screenpath(display: Lcd, screenpatch: ScreenPatch, modules_objects) -> None:

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


def setup(CONFIG):

    imported_modules = []

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
    tasks_group, modules_objects = setup_modules(
        CONFIG=CONFIG,
        imported_modules=imported_modules,
        screenpatch_collection=screenpatch_collection,
    )

    display.lcd_clear()

    return display, screen, imported_modules, modules_objects, screenpatch_collection


def main(display, screen, imported_modules, modules_objects, screenpatch_collection):

    while True:
        modules_execute_event_loop = asyncio.new_event_loop()
        tasks = []
        for module_object in modules_objects:

            # preexecuting async function
            module_execution_task = module_object.start()

            tasks.append(modules_execute_event_loop.create_task(module_execution_task))

        wait_tasks = asyncio.wait(tasks)

        modules_res = modules_execute_event_loop.run_until_complete(wait_tasks)
        for module_res in modules_res:

            if not len(module_res):
                continue

            module_output_arguments = list(module_res)[0].result()

            update_screenpath(
                display=display,
                modules_objects=modules_objects,
                screenpatch=module_output_arguments["screenpatch"],
            )

        modules_execute_event_loop.close()

        make_screenpatch_view(screen, screenpatch_collection, modules_objects)

        refresh_rate = 1
        time.sleep(refresh_rate - time.time() % refresh_rate)


if __name__ == "__main__":

    SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-1])
    CONFIG = get_config(SCRIPT_PATH)

    display, screen, imported_modules, modules_objects, screenpatch_collection = setup(
        CONFIG
    )
    main(display, screen, imported_modules, modules_objects, screenpatch_collection)
