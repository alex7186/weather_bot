# weather_bot

this program is built on asynchronous modules that display (connected to the raspberryPI via I2C) information about the 
* current date
* current time
* weather
* sunrise and sunset times

output to the display is carried out using libraries for interaction with i2C

the program itself is launched using the user's systemd service

---
**NOTE**

This script updates your Raspberry Pi OS !!! If you don't want to update the OS DO NOT USE THIS SCRIPT!

---

# Setting configuration
to insert telegram bot key:

1) go to file <br>
`<PATH_TO_PROJET_DIR>/misc/config.json`

2) put your openweather api key from https://openweathermap.org/ and edit following line: <br>
    `"OPENWEATHER_API_KEY" : "<YOUR_OPENWEATHER_API_KEY>".`

    (but if you don't feel like it, you can use my key)

3) put your screen parameters to the lines below:<br>
    `"LINES_COUNT" : <YOUR_SCREEN_LINES_COUNT>,`<br>
    `"LINE_LENGTH" : <YOUR_SCREEN_LINE_LENGTH - 1>,`

# Setup


after the following commands, this script will install the necessary libraries for working with the I2C interface and for interacting with the Internet

---

you need to connect your [display with i2c adapter](https://aliexpress.ru/item/1005001853905593.html?spm=a2g2w.productlist.search_results.1.13db1172pTCxgm&sku_id=12000017862865136) to RPi:
* display `SDA` -> GPIO 2
* display `SCL` -> GPIO 3
* display `GND` -> Rpi GND
* display `VCC` -> RPi 5v
<br><br>


run following commands to put the systemd service to the right place, make systemctl stuff, download dependencies and get things ready to run:

    cd <PATH_TO_PROJECT_DIR>
    make setup

# More about screen modules
each module is in its own folder inside the modules directory and has a main.py file.

inside main.py, each module contains class with method: <br>
`generate_screen_text`<br>
This method generates text for its screen area area defined in the settings file (according to module's refresh rate)

each module is entered into a 'config.json' file in the 'modules_data' section and has the following fields:
* `name` - module name for searching in `<PATH_TO_PROJECT_DIR>/modules/<name>`
* `refrash_skip_rate` - a number indicating how many screen refresh units (by default "GLOBAL_REFRASH_RATE" : 1) the module method `generate_screen_text` will be executed
* `rows`, `columns_start`, `columns_stop` - locates the module screen area (ScreenPatch)

# Screen modules example
## `dawn_time_dusk` module
this module is three lines by 9 characters. displays sunrise, sunset and current time data
```
╭――――――――――――――――――――╮
| 03:49:58           |
|➡️16:47:49           |
| 21:11:03           |
|                    |
╰――――――――――――――――――――╯
```

## `weather_block` module
this module is three lines by 9 characters. data of the current date, temperature, type of weather, day of the week are displayed
```
╭――――――――――――――――――――╮
|           11/06/23 |
|           +16 C°   |
|           Clear    |
|           Sun      |
╰――――――――――――――――――――╯
```

* Emoji characters from the screen test cases are displayed as `CustomCharacters` (5x8 pixels)

# Thanks to / Credits

* [script for python3.10 simple installation](https://github.com/tvdsluijs/sh-python-installer)

# License & Copyrights

Copyright (c) 2022 [itheo.tech](https://itheo.tech/) / Theo van der Sluijs

# MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Get your copy of the [MIT](https://choosealicense.com/licenses/mit/) License.