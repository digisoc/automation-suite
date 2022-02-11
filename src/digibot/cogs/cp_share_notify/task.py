""" Module Imports """
import asyncio
import random
import time
from datetime import date
from threading import Thread

import discord
import schedule
from discord.utils import get

""" Import Helpers """
from src.digibot.cogs.cp_share_notify.helpers import DATE_FORMAT, SCHEDULE_TYPE

""" Constants """
NOTIFY_TIME = "18:30"
MINUTE_TO_SEC = 60
REFRESH_RATE = 5 * MINUTE_TO_SEC

GREETINGS = ("Howdy", "Ni Hao", "Hola", "Bonjour", "Ciao", "Konichiwa", "Ola")


class CPTask:
    """CPShare Notifier Task"""

    def __init__(
        self,
        schedule: SCHEDULE_TYPE,
        server: discord.Guild = None,
    ):
        """Constructor for CPShare Notifier Task class"""
        self._schedule: SCHEDULE_TYPE = schedule
        self._server: discord.Guild = server
        self._active: bool = schedule != {}
        self.schedule_job()

    def schedule_job(self) -> None:
        """Starts a Notifier Job on a separate thread"""
        t = Thread(target=self._schedule_job)
        t.start()

    def _schedule_job(self) -> None:
        """Schedules a daily Notifier Job for the requested NOTIFY_TIME"""
        schedule.every().day.at(NOTIFY_TIME).do(self.schedule_job_sync)
        while True:
            schedule.run_pending()
            time.sleep(REFRESH_RATE)

    def schedule_job_sync(self) -> None:
        """Synchronous wrapper for schedule_notify"""
        # REF: https://stackoverflow.com/a/59645689
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.schedule_notify_async())
        loop.close()

    async def schedule_notify_async(self, notify_date: str = "") -> None:
        """
        Sends CPShare Notifications according to the active schedule

        Args:
            notify_date (str): users assigned to this date will be notified (OPTIONAL)
        """
        # ensure enabled
        if not self._active or not self._schedule or not self._server:
            return

        # notify users scheduled to CP share for given day
        failures = []
        notify_date = notify_date or date.today().strftime(DATE_FORMAT)
        users_to_notify = self._schedule[notify_date]
        for user in users_to_notify:
            # error check
            if not user:
                print(f"Invalid user detected in {self._schedule}")
                continue

            # get message parameters
            name = user["name"]
            member = self._server.get_member_named(name)
            greeting = random.choice(GREETINGS)
            event = user["event"]

            # send direct message
            dm = f"""{greeting} {name},
Just a quick reminder that today is your scheduled day to share DigiSoc's **{event}** event!

The prime time to change CP and share is 7-11 PM
You have the option to
1. Share CP (Write a short caption which includes the event link and rego link.)
2. Share Facebook Event (Write a short caption which includes the rego link.)
3. Invite 5 Friends
4. Create a Meme (Write a short caption which includes the event link, rego link, date and time)

Event CP's can be found on the Trello board :grin:"""

            try:
                await member.send(dm)
                print(f"Successfully sent reminder to {name}")
                await asyncio.sleep(0.5)
            except Exception as e:
                failures.append(f"{name} - {e}")

        # report failures to #requests
        if failures:
            request_channel = get(self._server.channels, name="requests")
            failure_report = "\n\t".join(failures)
            await request_channel.send(
                f"**CPShare Notifier**\nThe following users were not successfully notified:\n{failure_report}"
            )

    def get_schedule(self) -> SCHEDULE_TYPE:
        """Getter for CPShare Notifier Task schedule"""
        return self._schedule

    def set_schedule(self, schedule: SCHEDULE_TYPE) -> None:
        """Setter for CPShare Notifier Task schedule"""
        self._schedule = schedule

    def get_server(self) -> discord.Guild:
        """Getter for CPShare Notifier Task server"""
        return self._server

    def set_server(self, server: discord.Guild) -> None:
        """Getter for CPShare Notifier Task server"""
        self._server = server

    def get_status(self) -> bool:
        """Getter for CPShare Notifier Task active status"""
        return self._active

    def set_status(self, status: bool) -> None:
        """Setter for CPShare Notifier Task active status"""
        self._active = status
