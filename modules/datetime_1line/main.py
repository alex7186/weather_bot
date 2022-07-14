import asyncio
from datetime import datetime
from back.lcd.drivers import Lcd

from modules.base_screen_module import ScreenPatch, ScreenPatchModule
from back.text_formater import shift_center, shift_left, shift_right
from back.print_manager import mprint


class MainModule(ScreenPatchModule):
    def __init__(self, screenpatch: ScreenPatch, display: Lcd, CONFIG: dict) -> None:
        super().__init__(screenpatch, display)

    def get_date_string(self) -> str:
        cur_datetime = datetime.now()
        cur_hour = cur_datetime.hour
        cur_minute = cur_datetime.minute
        cur_second = cur_datetime.second

        res_text = ""
        res_text += shift_center(
            "{}.{}.{} {}:{}:{}".format(
                cur_datetime.year,
                cur_datetime.month,
                cur_datetime.day,
                cur_hour if cur_hour > 9 else "0" + str(cur_hour),
                cur_minute if cur_minute > 9 else "0" + str(cur_minute),
                cur_second if cur_second > 9 else "0" + str(cur_second),
            ),
            line_length=self.screenpatch.line_length,
        )

        return res_text

    async def setup(self):
        pass

    async def start(self):
        # def start(self):
        while True:
            date_text = shift_center(
                self.get_date_string(),
                line_length=self.screenpatch.line_length,
            )

            self.update_screenpath(date_text)

            await asyncio.sleep(1)
            # mprint('still working')


module: MainModule


async def module_start(screenpatch, display, CONFIG):
    global module
    module = MainModule(screenpatch=screenpatch, display=display, CONFIG=CONFIG)

    await module.setup()


async def module_execute():
    global module
    await module.start()
