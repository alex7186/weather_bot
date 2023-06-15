from smbus import SMBus
from RPi.GPIO import RPI_REVISION
from time import sleep
from re import match, search
from subprocess import check_output
from os.path import exists

from back.i2c_byte_codes import *


# old and new versions of the RPi have swapped the two i2c buses
# they can be identified by RPI_REVISION (or check sysfs)
BUS_NUMBER = 0 if RPI_REVISION == 1 else 1


class I2CDeviceError(Exception):
    pass


class I2CDevice:
    SLEEP_SHORT = 0.0001

    def __init__(self, addr=None, addr_default=None, bus=BUS_NUMBER):

        if addr:
            self.addr = addr

        else:
            # try autodetect address, else use default if provided
            try:
                if exists("/usr/sbin/i2cdetect"):
                    i2c_addresses = search(
                        "[0-9a-z]{2}(?!:)",
                        check_output(
                            ["/usr/sbin/i2cdetect", "-y", str(BUS_NUMBER)]
                        ).decode(),
                    )

                    self.addr = int("0x{}".format(i2c_addresses), base=16)

                else:
                    self.addr = addr_default

            except:
                self.addr = addr_default

        self.bus = SMBus(bus)

    def write_cmd(self, cmd):
        """write a single command"""
        try:
            self.bus.write_byte(self.addr, cmd)
            sleep(self.SLEEP_SHORT)
        except Exception:
            raise I2CDeviceError


class Lcd:
    SLEEP_SHORT = 0.0001
    SLEEP_MIDDLE = SLEEP_SHORT * 5
    SLEEP_LONG = 0.2

    def __init__(self, addr=None) -> None:

        self.addr = addr
        self.lcd = I2CDevice(addr=self.addr, addr_default=0x27)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)
        self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)

        sleep(self.SLEEP_LONG)

    def lcd_strobe(self, data):
        """clocks EN to latch command"""
        self.lcd.write_cmd(data | En | LCD_BACKLIGHT)
        sleep(self.SLEEP_MIDDLE)
        self.lcd.write_cmd(((data & ~En) | LCD_BACKLIGHT))
        sleep(self.SLEEP_SHORT)

    def lcd_write(self, cmd: int, mode: int = 0) -> None:
        """write a command to lcd"""

        def lcd_write_four_bits(self, data):
            self.lcd.write_cmd(data | LCD_BACKLIGHT)
            self.lcd_strobe(data)

        lcd_write_four_bits(self, mode | (cmd & 0xF0))
        lcd_write_four_bits(self, mode | ((cmd << 4) & 0xF0))

    def lcd_display_extended_string(self, string: str, line: int) -> None:
        """
        put extended string function. Extended string may contain placeholder like {0xFF} for
        displaying the CustomCharecters object
        """

        lines_address = [0x80, 0xC0, 0x94, 0xD4]

        try:
            self.lcd_write(lines_address[line])

            # Process the string
            while string:
                # Trying to find pattern {0xFF} representing a symbol
                has_custom_charecter = match(r"\{0[xX][0-9a-fA-F]{2}\}", string)
                if has_custom_charecter:
                    self.lcd_write(int(has_custom_charecter.group(0)[1:-1], 16), Rs)
                    string = string[6:]
                else:
                    self.lcd_write(ord(string[0]), Rs)
                    string = string[1:]
        except Exception:
            raise I2CDeviceError
