""" Module Imports """
import asyncio
import random
import time
from datetime import date
from threading import Thread
from typing import DefaultDict, Dict

import discord
import schedule
from discord.ext import commands
from discord.utils import get

from src.digibot.cogs.event_thread.cogs import REQUESTS_CHANNEL
from src.loop import get_loop

""" Import Helpers """
from src.digibot.cogs.cp_share_notify.helpers import DATE_FORMAT, SCHEDULE_TYPE

""" Constants """
# TODO: 30 minutes before PRIME time lower bound?
NOTIFY_TIME = "18:30"
# Refresh every 60 seconds (1 minute)
REFRESH_RATE = 60

GREETINGS = ("Howdy", "Ni Hao", "Hola", "Bonjour", "Ciao", "Konichiwa", "Ola")


class CPTask:
    """CPShare Notifier Task"""

    def __init__(
        self,
        schedule: SCHEDULE_TYPE,
        client: commands.Bot,
    ):
        """Constructor for CPShare Notifier Task class"""
        self._schedule: SCHEDULE_TYPE = schedule
        self._client: commands.Bot = client
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
        loop = get_loop()
        future = asyncio.run_coroutine_threadsafe(self.schedule_notify_async(), loop)
        future.result()

    async def schedule_notify_async(self, notify_date: str = "") -> None:
        """
        Sends CPShare Notifications according to the active schedule

        Args:
            notify_date (str): users assigned to this date will be notified (OPTIONAL)
        """
        # ensure enabled
        if not self._active:
            return

        # notify users scheduled to CP share for given day
        servers = self._get_servers()
        feedback = DefaultDict(lambda: DefaultDict(list))
        notify_date = notify_date or date.today().strftime(DATE_FORMAT)
        users_to_notify = self._schedule.get(notify_date, [])
        for user in users_to_notify:
            # error check
            if not user:
                print(f"Invalid user detected in {self._schedule}")
                continue

            # get message parameters
            name = user["name"]
            server_id = user["server_id"]
            server = servers[server_id]
            member = server.get_member_named(name)
            greeting = random.choice(GREETINGS)
            event = user["event"]

            # send direct message
            dm = f"""{greeting} {name},
Just a quick reminder that today is your scheduled day to share DigiSoc's **{event}** event!

The prime time to change CP and share is 7-11 PM
You have the option to
1. Share CP (Write a short caption which includes the event link and rego link.)
2. Share Facebook Event (Write a short caption which includes the rego link.)
3. Create a Meme (Write a short caption which includes the event link, rego link, date and time)

Event CP's can be found on the Trello board :grin:"""

            try:
                await member.send(dm)
                print(f"Successfully sent reminder to {name}")
                feedback[server]["success"].append(name)
                await asyncio.sleep(0.5)
            except Exception:
                feedback[server]["failures"].append(name)

        # report status to #requests
        for server, statuses in feedback.items():
            success = statuses["success"]
            failures = statuses["failures"]
            if not success and not failures:
                continue

            success_names = "\n".join("\t" + name for name in success)
            success_report = (
                f"Successfully sent reminders to:\n{success_names}" if success else ""
            )
            failure_names = "\n".join("\t" + name for name in failures)
            failure_report = (
                f"Failed to send reminders to:\n{failure_names}" if failures else ""
            )

            report = success_report + "\n" + failure_report
            if report.isspace():
                continue

            # send report to requests channel
            request_channel = get(server.channels, name=REQUESTS_CHANNEL)
            if request_channel is None:
                print(f"Could not find #{REQUESTS_CHANNEL} channel in {server.name}")
            else:
                await request_channel.send("**CPShare Notifier**\n" + report)

    def _get_servers(self) -> Dict[int, discord.Guild]:
        """
        Gets all the servers the bot is in

        Returns:
            servers (dict): maps guild id (int) -> guild objects (discord.Guild)
        """
        guilds = self._client.guilds
        servers = {}
        for guild in guilds:
            servers[guild.id] = guild
        return servers

    def get_schedule(self) -> SCHEDULE_TYPE:
        """Getter for CPShare Notifier Task schedule"""
        return self._schedule

    def set_schedule(self, schedule: SCHEDULE_TYPE) -> None:
        """Setter for CPShare Notifier Task schedule"""
        self._schedule = schedule

    def add_schedule(self, schedule: SCHEDULE_TYPE) -> None:
        """Adds another schedule to the current CPShare Notifier Task schedule"""
        for key, value in schedule.items():
            self._schedule[key].extend(value)

    def get_status(self) -> bool:
        """Getter for CPShare Notifier Task active status"""
        return self._active

    def set_status(self, status: bool) -> None:
        """Setter for CPShare Notifier Task active status"""
        self._active = status
