from crontab import CronTab
import sys
import os

from config_manager import get_config

# takes "start" or "stop" as execution argument
args = list(sys.argv)[1:]

SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-2])
CONFIG = get_config(SCRIPT_PATH)


cron = CronTab(user=True)


def delete_cron_job(APP_NAME: str, cron: CronTab):

    for existing_job in cron:
        if existing_job.comment.strip() == APP_NAME:
            cron.remove(existing_job)


# if input arg is "start" then add to cron_table
if "start" in args:

    delete_cron_job(CONFIG["APP_NAME"], cron)

    job = cron.new(
        command=f"python3.10 {SCRIPT_PATH}/app.py", comment=CONFIG["APP_NAME"]
    )

    job.setall(CONFIG["CRONTAB_SETUP"])

    cron.write()

# if input arg is "stop" then remove from cron_table
elif "stop" in args:

    delete_cron_job(CONFIG["APP_NAME"], cron)

    cron.write()
