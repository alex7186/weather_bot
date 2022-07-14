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

    def __init__(self, screenpatch: ScreenPatch, display: Lcd) -> None:
        self.screenpatch = screenpatch
        self.current_text: str = ""
        self.display = display

    def _check_screenpatch_text(self, new_text: str) -> bool:

        # new_text_splitted = new_text.split('\n')
        # max_text_length = list(map(len, new_text_splitted))
        # print(f"{new_text_splitted=}")
        # print(f"{max_text_length=}")

        # if len(new_text_splitted) > len(self.screenpatch.rows):
        #     raise ValueError(
        #         f"can`t put text |{new_text_splitted}| to patch with rows {self.screenpatch.rows}"
        #     )
        # elif max_text_length > self.screenpatch.line_length + 1:
        #     raise ValueError(
        #         f"can`t put text |{new_text_splitted}| with max len {max_text_length} \
        #         to patch with line length {self.screenpatch.line_length}"
        #     )

        self.current_text = new_text
        return True

    def update_screenpath(self, new_text: str) -> None:

        self._check_screenpatch_text(new_text)  # new text checking procedure

        new_text_splitted = new_text.split("\n")

        for i, row in enumerate(self.screenpatch.rows):

            self.display.lcd_display_string(
                shift_center(
                    new_text_splitted[i],
                    line_length=self.screenpatch.line_length,
                ),
                row + 1,
            )

        # new_text_splitted = new_text.split('\n')

        # # for i in range(len(current_text_splitted)):
        # #     current_text_splitted[i] = shift_center(
        # #         self.current_text.split('\n')[i], self.screenpatch.line_length
        # #     )

        # for i, row in enumerate(self.screenpatch.rows):

        #     self.display.lcd_display_string(
        #         new_text_splitted[i][:self.screenpatch.line_length],
        #         row + 1
        #     )

    def get_screenpatch_text(self) -> str:
        return self.current_text

    async def setup(self):
        raise NotImplementedError

    async def start(self):
        raise NotImplementedError
