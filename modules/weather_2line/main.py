import asyncio
from back.lcd.drivers import Lcd

from modules.base_screen_module import ScreenPatch, ScreenPatchModule
from back.weather_formater import format_weather
from back.weather_api_service import Weather, get_weather
from back.coordinates import Coordinates, get_coords
from back.exceptions import ApiServiceError, CantGetCoordinates
from back.print_manager import mprint


def get_weather_safe(coordinates, CONFIG):
    try:
        weather = get_weather(coordinates, CONFIG)
    except ApiServiceError as e:
        mprint(f"Не удалось получить погоду по координатам {coordinates}")
        weather = Weather()
        exit(1)

    return weather


class MainModule(ScreenPatchModule):
    def __init__(
        self, screenpatch: ScreenPatch, refrash_skip_rate: int, CONFIG: dict
    ) -> None:

        super().__init__(
            screenpatch,
        )
        self.refrash_skip_rate = refrash_skip_rate
        self.execution_count = 0

        self.CONFIG = CONFIG

    def get_weather_string(self) -> str:
        try:
            coordinates = get_coords()
        except CantGetCoordinates:
            mprint("Не удалось получить GPS координаты")

        weather = get_weather_safe(coordinates, self.CONFIG)

        res_text = format_weather(weather, self.screenpatch)

        return res_text

    async def start(self):

        self.execution_count = self.execution_count % self.refrash_skip_rate

        if self.execution_count != 0:

            self.execution_count += 1
            return {"screenpatch": self.screenpatch, "new_text": ""}

        self.set_screenpatch_text(self.get_weather_string())

        self.execution_count += 1
        return {
            "screenpatch": self.screenpatch,
            "new_text": self.get_screenpatch_text(),
        }
