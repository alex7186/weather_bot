from back.i2c_manager import CustomCharacters
from back.print_manager import mprint

from modules.base_screen_module import ScreenPatch, ScreenPatchModule

from modules.weather_1line.back.weather_formater import format_weather
from modules.weather_1line.back.weather_api_service import Weather, get_weather
from modules.weather_1line.back.coordinates import Coordinates, get_coords
from modules.weather_1line.back.exceptions import ApiServiceError, CantGetCoordinates


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

        self.CONFIG = CONFIG

    async def generate_screen_text(self) -> str:
        try:
            coordinates = get_coords()
        except CantGetCoordinates:
            mprint("Не удалось получить GPS координаты")

        weather = get_weather(coordinates, self.CONFIG)

        res_text = format_weather(weather, self.screenpatch)

        return res_text
