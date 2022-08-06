from back.lcd.drivers import CustomCharacters


from modules.base_screen_module import ScreenPatch, ScreenPatchModule

from modules.sun_2line.back.sun_formater import format_sun
from modules.sun_2line.back.weather_api_service import get_sun
from modules.sun_2line.back.coordinates import get_coords


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

        sun_periods = get_sun(coordinates, self.CONFIG)

        return format_sun(sun_periods, self.screenpatch, self.custom_charecters)
