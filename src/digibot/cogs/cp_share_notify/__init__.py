""" Module Imports """
import os
import json
import discord
from discord.ext import commands

""" Helper Imports """
from src.digibot.cogs.cp_share_notify.task import CPTask
from src.digibot.cogs.cp_share_notify.helpers import parse_schedule

""" Constants """
SCHEDULES_DIR = "src/digibot/cogs/cp_share_notify/schedules"
if not os.path.exists(SCHEDULES_DIR):
    os.mkdir(SCHEDULES_DIR)

NOTIFIER_INACTIVE = "No CPShare Schedule Notifier active :crying_cat_face:"

# cp_commands = commands.Group("cp")


class CPNotifier(commands.Cog):
    """CPShare Schedule Notifier"""

    def __init__(self, client: commands.Bot) -> None:
        self._client: commands.Bot = client
        self._task: CPTask = CPTask({})

    def is_active(self) -> bool:
        """Returns whether a CPNotifier has an active CPTask"""
        return self._task.get_status()

    @commands.command()
    async def notifier_status(self, ctx: commands.Context) -> None:
        """Returns the current notifier status"""
        if self.is_active():
            await ctx.message.add_reaction("✅")
            await ctx.reply(json.dumps(self._task.get_schedule(), indent=2))
        else:
            await ctx.message.add_reaction("❓")
            await ctx.reply(NOTIFIER_INACTIVE)

    @commands.command()
    @commands.has_any_role("axie", "Marketing", "Execs")
    async def notifier_manual(
        self, ctx: commands.Context, notify_date: str = ""
    ) -> None:
        """(PLEASE AVOID!!) Manually invokes notifier for given day (default: current day)"""
        if self.is_active():
            await self._task.schedule_notify(notify_date)
            await ctx.message.add_reaction("✅")
        else:
            await ctx.reply(NOTIFIER_INACTIVE)

    @commands.command()
    async def notifier_set(self, ctx: commands.Context) -> None:
        """
        Starts a notifier for an attached .csv CPShare Schedule
        (attach or reply to a message with an attached schedule)
        """
        # determine type of request
        attachments = ctx.message.attachments
        message_reference = ctx.message.reference

        if not attachments and not message_reference:
            # invalid format
            await ctx.message.add_reaction("❌")
            await ctx.reply(
                "Please attach or reply to a message with an attached schedule"
            )

        elif not attachments:
            # message reply -> extract attachment from original reference
            await self._notifier_set(message_reference, ctx.guild)
            await ctx.message.add_reaction("✅")

        else:
            # extract attachment from message
            await self._notifier_set(ctx.message, ctx.guild)

    async def _notifier_set(
        self, message: discord.Message, server: discord.Guild
    ) -> None:
        """Extract and parse .csv CPShare Schedule file in message"""
        # validate and save csv attachment
        attachment = message.attachments[0]
        file_name = f"{SCHEDULES_DIR}/{attachment.filename}"
        if not file_name.endswith(".csv"):
            # NOTE: may need file validation to confirm csv contents
            return
        await attachment.save(file_name)

        # parse schedule and create Notifier Task
        schedule = parse_schedule(file_name)
        self._task.set_schedule(schedule)
        self._task.set_server(server)
        self._task.set_status(True)

        await message.add_reaction("✅")

    @commands.command()
    async def notifier_disable(self, ctx: commands.Context) -> None:
        """Cancels the current running Notifier task"""
        if self.is_active():
            self._task.set_status(False)
            await ctx.message.add_reaction("✅")
        else:
            await ctx.message.add_reaction("❌")
            await ctx.reply(NOTIFIER_INACTIVE)


def setup(client: commands.Bot) -> None:
    client.add_cog(CPNotifier(client))