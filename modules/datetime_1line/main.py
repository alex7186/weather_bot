from datetime import datetime
from back.i2c_dev import CustomCharacters

from modules.base_screen_module import ScreenPatch, ScreenPatchModule
from back.text_formater import shift_center, shift_left, shift_right


class MainModule(ScreenPatchModule):
    def __init__(
        self,
        screenpatch: ScreenPatch,
        refrash_skip_rate: int,
        CONFIG: dict,
        custom_charecters: CustomCharacters,
    ) -> None:
        super().__init__(screenpatch)

        self.refrash_skip_rate = refrash_skip_rate
        self.execution_count = 0

    async def generate_screen_text(self) -> str:
        cur_datetime = datetime.now()
        cur_hour = cur_datetime.hour
        cur_minute = cur_datetime.minute
        cur_second = cur_datetime.second

        res_text = ""

        res_text += shift_left(
            "{}.{}.{}".format(
                cur_datetime.year,
                cur_datetime.month
                if cur_datetime.month > 9
                else "0" + str(cur_datetime.month),
                cur_datetime.day
                if cur_datetime.day > 9
                else "0" + str(cur_datetime.day),
            ),
            line_length=self.screenpatch.line_length,
        )

        cur_minute += 3

        res_text += shift_right(
            "{}:{}:{}".format(
                cur_hour if cur_hour > 9 else "0" + str(cur_hour),
                cur_minute if cur_minute > 9 else "0" + str(cur_minute),
                cur_second if cur_second > 9 else "0" + str(cur_second),
            ),
            line_length=self.screenpatch.line_length,
        )

        return res_text
