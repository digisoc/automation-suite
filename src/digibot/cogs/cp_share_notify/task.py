""" Module Imports """
import time
import random
import discord
import asyncio
import schedule
from datetime import date
from threading import Thread
from discord.utils import get

""" Import Helpers """
from src.digibot.cogs.cp_share_notify.helpers import DATE_FORMAT, SCHEDULE_TYPE

""" Constants """
NOTIFY_TIME = "18:30"
MINUTE_TO_SEC = 60
REFRESH_RATE = 5 * MINUTE_TO_SEC

GREETINGS = ("Howdy", "Ni Hao", "Hola", "Bonjour", "Ciao", "Konichiwa", "Ola")


# NOTE: Notifier
class CPTask:
    def __init__(
        self,
        schedule: SCHEDULE_TYPE,
        server: discord.Guild = None,
        active: bool = False,
    ):
        """Constructor for CP Notifier Task class"""
        self._schedule: SCHEDULE_TYPE = schedule
        self._server: discord.Guild = server
        self._active: bool = active
        self.schedule_job()

    def schedule_job(self) -> None:
        """Starts a Notifier Job on a separate thread"""
        t = Thread(target=self.schedule_job)
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
        Sends CP Share Notifications according to the active schedule

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
            share_type = user["share_type"]
            event = user["event"]

            # send direct message
            dm = f"{greeting} {name},\n\nJust a quick reminder that today is your scheduled day to share a **{share_type}** for DigiSoc's **{event}** event!\n\nHot tip: prime time for sharing seems to be around 7-9pm, and event CP's can be found on the Trello board :grin:"
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
                f"**CP Notifier**\nThe following users were not successfully notified:\n{failure_report}"
            )

    def get_schedule(self) -> SCHEDULE_TYPE:
        """Getter for CP Notifier Task schedule"""
        return self._schedule

    def set_schedule(self, schedule: SCHEDULE_TYPE) -> None:
        """Setter for CP Notifier Task schedule"""
        self._schedule = schedule

    def get_server(self) -> discord.Guild:
        """Getter for CP Notifier Task server"""
        return self._server

    def set_server(self, server: discord.Guild) -> None:
        """Getter for CP Notifier Task server"""
        self._server = server

    def get_status(self) -> bool:
        """Getter for CP Notifier Task active status"""
        return self._active

    def set_status(self, status: bool) -> None:
        """Setter for CP Notifier Task active status"""
        self._active = status
