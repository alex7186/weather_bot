from back.coords_manager import get_coords
from back.weather_cache_mananger import get_weather
from back.custom_charecters_manager import CustomCharacters, CHARS_SET

from modules.base_screen_module import ScreenPatch
from modules.test_module.formater import load_custom_charecters


class MainModule(ScreenPatch):
    def __init__(
        self,
        rows: int,
        columns_start: int,
        columns_stop: int,
        refrash_skip_rate: int,
        CONFIG: dict,
        custom_charecters: CustomCharacters,
    ) -> None:

        super().__init__(
            rows=rows,
            columns_start=columns_start,
            columns_stop=columns_stop,
        )

        self.refrash_skip_rate = refrash_skip_rate
        self.execution_count = 0
        self.custom_charecters = load_custom_charecters(
            custom_charecters=custom_charecters, CHARS_SET=CHARS_SET
        )

        self.CONFIG = CONFIG

    async def generate_screen_text(self) -> str:

        res_text = ["t" * self.screenpatch.line_length] * len(self.screenpatch.rows)

        return "\n".join(res_text)
