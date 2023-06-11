import asyncio
from importlib import import_module as importlib_import_module
from typing import Any

from back.custom_charecters_manager import CustomCharacters
from back.print_manager import mprint

from modules.base_screen_module import ScreenPatch


def import_modules(
    modules_list: list,
    CONFIG: dict,
    screenpatch_collection: list[ScreenPatch],
    custom_charecters: CustomCharacters,
) -> list[Any]:
    """
    import all "main.py" files
    by template <SCRIPT_PATH>/modules/module_1/main.py
    """

    modules_path_list = [f"modules.{module_name}.main" for module_name in modules_list]
    APP_NAME = "import_manager"

    imported_modules: list[Any] = []
    for i, module_instance in enumerate(modules_path_list):
        imported_modules.append(importlib_import_module(module_instance))
        mprint(APP_NAME + " " + f": Imported {modules_list[i]}")

    modules_objects = []
    refrash_skip_rates = list(
        map(lambda x: x["refrash_skip_rate"], CONFIG["modules_data"])
    )

    for i, module_instance in enumerate(imported_modules):
        modules_objects.append(
            module_instance.MainModule(
                rows=screenpatch_collection[i].rows,
                columns_start=screenpatch_collection[i].columns_start,
                columns_stop=screenpatch_collection[i].columns_stop,
                refrash_skip_rate=refrash_skip_rates[i],
                CONFIG=CONFIG,
                custom_charecters=custom_charecters,
            )
        )

    return modules_objects


def custom_exception_handler(loop, context):
    # first, handle with default handler
    loop.default_exception_handler(context)

    # TODO process some more exceptions
    # exception = context.get("exception")
    # if isinstance(exception, ZeroDivisionError):
    #     mprint(context)
    #     loop.stop()
    #     # loop.close()


def execute_modules(
    modules_objects: list[Any],
) -> tuple[set[asyncio.Task[Any]], set[asyncio.Task[Any]]]:

    modules_execute_event_loop = asyncio.new_event_loop()
    modules_execute_event_loop.set_exception_handler(custom_exception_handler)

    tasks = []
    for module_object in modules_objects:

        # preexecuting async function
        module_execution_task = module_object.start()

        tasks.append(modules_execute_event_loop.create_task(module_execution_task))

    wait_tasks = asyncio.wait(tasks)

    return modules_execute_event_loop.run_until_complete(wait_tasks)
