# from typing import NamedTuple
from back.lcd.drivers import Lcd
from back.text_formater import shift_center


class ScreenPatch:
    """Square space on the screen"""

    def __init__(self, rows: list = [], columns_start: int = 0, columns_stop: int = -1):
        self.rows = rows
        self.columns_start = columns_start
        self.columns_stop = columns_stop

        self.columns = (columns_start, columns_stop)
        self.line_length = columns_stop - columns_start


class ScreenPatchModule:
    """Patch screen manager module"""

    def __init__(self, screenpatch: ScreenPatch) -> None:
        self.screenpatch = screenpatch
        self.current_text: str = ""

    def set_screenpatch_text(self, new_text):
        self.current_text = new_text

    def get_screenpatch_text(self) -> str:
        return self.current_text

    async def setup(self):
        pass

    async def start(self):
        raise NotImplementedError
