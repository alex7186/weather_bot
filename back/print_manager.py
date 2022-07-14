import logging


logging.basicConfig(
    filename=f"/home/pi/scripts/weather_bot/misc/logfile.txt",
    filemode="a",
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


def mprint(message):
    try:
        print(message)
        logging.info(message)

    except Exception as e:
        pass
