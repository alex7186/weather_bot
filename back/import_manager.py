import asyncio
from datetime import datetime
from importlib import import_module

from back.lcd.drivers import Lcd
from back.print_manager import mprint


def import_modules(modules_list):
    """
    import all "main.py" files
    by template <SCRIPT_PATH>/modules/module_1/main.py
    """

    modules_path_list = [f"modules.{module_name}.main" for module_name in modules_list]
    APP_NAME = "import_manager"

    imported_modules = []
    for i, module in enumerate(modules_path_list):
        imported_modules.append(import_module(module))
        mprint(APP_NAME + " " + f": Imported {modules_list[i]}")

    return imported_modules


def setup_modules(CONFIG, imported_modules, screenpatch_collection: list):

    modules_init_event_loop = asyncio.new_event_loop()
    tasks = []
    modules_objects = []
    refrash_skip_rates = list(
        map(lambda x: x["refrash_skip_rate"], CONFIG["modules_data"])
    )

    for i, module in enumerate(imported_modules):
        modules_objects.append(
            module.MainModule(
                screenpatch=screenpatch_collection[i],
                refrash_skip_rate=refrash_skip_rates[i],
                CONFIG=CONFIG,
            )
        )

        tasks.append(modules_init_event_loop.create_task(modules_objects[i].setup()))

        date = ".".join(
            str(el) for el in list(datetime.now().date().timetuple())[:3][::-1]
        )
        time = str(datetime.now().time()).split(".")[0]
        date = time + " " + date

    tasks = asyncio.wait(tasks)
    tasks_group = asyncio.gather(tasks)

    modules_init_event_loop.run_until_complete(tasks)
    modules_init_event_loop.close()

    return tasks_group, modules_objects
