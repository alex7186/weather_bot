# weather_bot

# Setting configuration
to insert telegram bot key:

1) go to file <br>
`<PATH_TO_PROJET_DIR>/misc/config.json`

2) put your openweather api key from https://openweathermap.org/ and edit following line: 
    `"OPENWEATHER_API_KEY" : "<YOUR_OPENWEATHER_API_KEY>".`

3) put your screen parameters to the lines below:
    `"LINES_COUNT" : <YOUR_SCREEN_LINES_COUNT>,`
    `"LINE_LENGTH" : <YOUR_SCREEN_LINE_LENGTH - 1>,`

# Setup
you need to connect your [display with i2c adapter](https://aliexpress.ru/item/1005001853905593.html?spm=a2g2w.productlist.search_results.1.13db1172pTCxgm&sku_id=12000017862865136) to RPi:
* display `SDA` -> GPIO 2
* display `SCL` -> GPIO 3
* display `GND` -> Rpi GND
* display `VCC` -> RPi 5v
<br><br>


run following commands to put the systemd service to the right place, make systemctl stuff, download dependencies and get things ready to run:

`cd <PATH_TO_PROJECT_DIR>`<br>
`make setup`

# Screen modules
each module is in its own folder inside the modules directory and has a main.py file.

inside main.py, each module contains class with method: <br>
`generate_screen_text`<br>
This method generates text for its screen area area defined in the settings file (according to module's refresh rate)

each module is entered into a 'config.json' file in the 'modules_data' section and has the following fields:
* `name` - module name for searching in `<PATH_TO_PROJECT_DIR>/modules/<name>`
* `refrash_skip_rate` - a number indicating how many screen refresh units (by default "GLOBAL_REFRASH_RATE" : 1) the module method `generate_screen_text` will be executed
* `rows`, `columns_start`, `columns_stop` - locates the module screen area (ScreenPatch)


