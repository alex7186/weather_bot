from back.coords_manager import get_coords
from back.weather_cache_mananger import get_weather
from back.custom_charecters_manager import CustomCharacters, CHARS_SET

from modules.base_screen_module import ScreenPatch, ScreenPatchModule
from modules.full_screen_monolite.back.full_screen_formater import (
    format_full_screen,
    load_custom_charecters,
)


class MainModule(ScreenPatchModule):
    def __init__(
        self,
        screenpatch: ScreenPatch,
        refrash_skip_rate: int,
        CONFIG: dict,
        custom_charecters: CustomCharacters,
    ) -> None:

        super().__init__(
            screenpatch,
        )
        self.refrash_skip_rate = refrash_skip_rate
        self.execution_count = 0
        self.custom_charecters = load_custom_charecters(
            custom_charecters=custom_charecters, CHARS_SET=CHARS_SET
        )

        self.CONFIG = CONFIG

    async def generate_screen_text(self) -> str:
        coordinates = get_coords()

        weather, sun_periods = get_weather(coordinates, self.CONFIG)

        res_text = format_full_screen(
            weather=weather,
            sun_periods=sun_periods,
            custom_charecters=self.custom_charecters,
        )

        return res_text
