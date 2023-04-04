from back.custom_charecters_manager import CustomCharacters
from back.coords_manager import get_coords
from back.cache_mananger import get_weather

from modules.base_screen_module import ScreenPatch, ScreenPatchModule
from modules.sun_2line.back.sun_formater import format_sun


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
        self.custom_charecters = custom_charecters

        self.CONFIG = CONFIG

    async def generate_screen_text(self) -> str:

        coordinates = get_coords()

        _, sun_periods = get_weather(coordinates, self.CONFIG)

        res_text = format_sun(sun_periods, self.screenpatch, self.custom_charecters)

        return res_text
