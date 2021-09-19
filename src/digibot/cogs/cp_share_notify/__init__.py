""" Module Imports """
import os
import schedule
import discord
from discord.ext import commands
from discord.utils import get
from threading import Thread
from datetime import date

""" Helper Imports """
from src.digibot.cogs.cp_share_notify.helpers import parse_schedule


""" Constants """
SCHEDULES_DIR = "src/digibot/cogs/cp_share_notify/schedules"
if not os.path.exists(SCHEDULES_DIR):
    os.mkdir(SCHEDULES_DIR)

GREETINGS = {"Howdy", "Ni Hao", "Hola", "Bonjour", "Ciao", "Konichiwa", "Ola"}
NOTIFY_TIME = "18:30"


# cp_commands = commands.Group("cp")


class CPShare(commands.Cog):
    def __init__(self, client: commands.bot.Bot) -> None:
        self._client: commands.bot.Bot = client
        self._active_schedule = {}
        self._active_notify = None  # thread
        self._active_guild = None

    @commands.command()
    async def schedule_status(self, ctx: commands.context.Context) -> None:
        """Gets the current schedule status"""
        await ctx.reply(
            self._active_schedule if self._active_notify else "No notifier running"
        )

    @commands.command()
    @commands.has_any_role("axie", "Marketing", "Execs")
    async def schedule_notify_manual(
        self, ctx: commands.context.Context, day: str
    ) -> None:
        """Manually send notifications for current day (PLEASE AVOID)"""
        # remove active thread
        # schedule_notify()
        await self._schedule_notify(day)

    async def _schedule_notify(self, day=date.today()) -> None:
        task = self._active_schedule
        if not task:
            return
        # get current date
        current_date = day.strftime("%Y-%m-%d")
        current_year = current_date[:4]

        # get DigiSoc Team server
        server = get(self._client.guilds, name=f"DigiSoc Team {current_year}")
        if not server:
            raise Exception(
                f"Could not find connected DigiSoc Team {current_year} server for CP Scheduling"
            )

        # notify users scheduled to CP share today
        failures = []
        users_to_notify = task[current_date]
        for user in users_to_notify:
            name = user["name"]
            user = server.get_member_named(name)
            greeting = random.choice(GREETINGS)
            share_type = user["share_type"]
            event = user["event"]

            # send message
            dm = f"{greeting} {name},\n\nJust a quick reminder that today is your scheduled day to share a **{share_type}** for DigiSoc's **{event}** event!\n\nHot tip: prime time for sharing seems to be around 7-9pm, and event CP's can be found on the Trello board :grin:"
            try:
                # await user.send(dm)
                print(f"Successfully sent reminder to {name}")
            except Exception as e:
                failures.append((name, e))

        # send failures to axie

        # thread

    @commands.command()
    async def schedule_add(self, ctx: commands.context.Context) -> None:
        """Starts a notifier for an attached .csv CP Schedule"""
        # validate and save csv attachment
        attachments = ctx.message.attachments
        if not attachments:
            return
        attachment = attachments[0]
        file_name = f"{SCHEDULES_DIR}/{attachment.filename}"
        if not file_name.endswith(".csv"):
            # TODO: may need file validation to confirm csv
            return
        await attachment.save(file_name)

        # parse schedule
        self._active_schedule = parse_schedule(file_name)

        # schedule notify
        schedule.every().day.at(NOTIFY_TIME).do(self._schedule_notify)

    @commands.command()
    async def schedule_remove(self, ctx: commands.context.Context) -> None:
        # TODO: remove thread
        pass


def setup(client: commands.bot.Bot) -> None:
    client.add_cog(CPShare(client))
