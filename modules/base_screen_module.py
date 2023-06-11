class ScreenPatch:
    """Square space on the screen"""

    def __init__(
        self, rows: list = [], columns_start: int = 0, columns_stop: int = -1
    ) -> None:

        self.rows = rows
        self.columns_start = columns_start
        self.columns_stop = columns_stop

        self.current_text: str = ""

    def set_screenpatch_text(self, new_text):
        self.current_text = new_text

    def get_screenpatch_text(self) -> str:
        return self.current_text

    async def generate_screen_text(self) -> str:
        raise NotImplementedError

    async def start(self):
        self.execution_count = self.execution_count % self.refrash_skip_rate

        if self.execution_count == 0:
            self.set_screenpatch_text(await self.generate_screen_text())

        self.execution_count += 1
        return {
            "new_text": self.get_screenpatch_text(),
        }
