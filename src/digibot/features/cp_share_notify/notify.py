""" Module Imports """
import os
import discord
import random
from datetime import date

""" Import Helpers """
from .helpers import parse_schedule

""" CSV Schedules Directory """
SCHEDULES_DIR = "./schedules"
if not os.path.exists(SCHEDULES_DIR):
    os.mkdir(SCHEDULES_DIR)


""" CONSTANTS """
GREETINGS = {"Howdy", "Ni Hao", "Hola", "Bonjour", "Ciao", "Konichiwa", "Ola"}


""" Active CP Schedule """
active_schedule = {}


async def update_schedule(message: discord.Message) -> None:
    # retrieve csv from message
    attachments = message.attachments

    # save to SCHEDULES_DIR

    # parse csv to obtain schedule
    new_schedule = parse_schedule(message.content)

    # update cp task
    # task = par

    pass


def scheduled_notify() -> None:
    # NOTE: will need Discord ID's of users
    # no active task
    if not active_schedule:
        return

    # get current date
    today = date.today()
    current_date = today.strftime("%Y-%m-%d")

    # notify users scheduled to CP share today
    users_to_notify = task[current_date]
    for user in users_to_notify:
        name = user["name"]  # and get user id by user name
        greeting = random.choice(GREETINGS)
        share_type = user["share_type"]
        event = user["event"]
        dm = f"{greeting} {name},\n\nJust a quick reminder that today is your scheduled day to share a **{share_type}** for DigiSoc's **{event}** event!\n\nHot tip: prime time for sharing seems to be around 7-9pm, and event CP's can be found on the Trello board :grin:"
        # send
