import json

from back.i2c_manager import Rs


def v_invert(custom_charecter: list[list[str]]) -> list[list[str]]:
    return custom_charecter[::-1]


def h_invert(custom_charecter: list[list[str]]) -> list[list[str]]:
    return list(map(lambda x: x[::-1], custom_charecter))


CHARS_SET = []
with open(f"misc/custom_chars.json", "r") as f:
    CHARS_SET = json.load(f)


class CustomCharacters:
    def __init__(self, lcd):
        self.lcd = lcd
        # Data for custom characters #1-#8. Code {0x00}-{0x07}.
        # It's just colored squares by default

        self.chars = dict(zip([el for el in range(8)], [["1" * 5] * 8] * 8))
        self.current_index = 0

    def append(self, data: list) -> str:
        if self.current_index < 7:

            self.chars[self.current_index] = data
            self.current_index += 1
            return "{0x0" + str(self.current_index - 1) + "}"
        else:
            raise IndexError

    def load_custom_characters_data(self):

        # commands to load character adress to RAM srarting from desired base adresses:
        char_load_cmds = [0x40, 0x48, 0x50, 0x58, 0x60, 0x68, 0x70, 0x78]
        for char_num in range(8):

            # command to start loading data into CG RAM:
            self.lcd.lcd_write(char_load_cmds[char_num])

            for line_num in range(8):

                line = self.chars[char_num][line_num]
                binary_str_cmd = "0b000{0}".format(line)
                self.lcd.lcd_write(int(binary_str_cmd, 2), Rs)
