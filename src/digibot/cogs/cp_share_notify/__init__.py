""" Module Imports """
import os
import discord
from discord.ext import commands

""" Helper Imports """
from src.digibot.cogs.cp_share_notify.task import CPTask
from src.digibot.cogs.cp_share_notify.helpers import parse_schedule

""" Constants """
SCHEDULES_DIR = "src/digibot/cogs/cp_share_notify/schedules"
if not os.path.exists(SCHEDULES_DIR):
    os.mkdir(SCHEDULES_DIR)

NOTIFIER_INACTIVE = "No CP Share Schedule Notifier active :crying_cat_face:"

# cp_commands = commands.Group("cp")


class CPNotifier(commands.Cog):
    """CP Share Notifier"""

    def __init__(self, client: commands.bot.Bot) -> None:
        self._client: commands.bot.Bot = client
        self._task: CPTask = CPTask({})

    def is_active(self) -> bool:
        """Returns whether a CPNotifier has an active CPTask"""
        return self._task.get_status()

    @commands.command()
    async def notifier_status(self, ctx: commands.context.Context) -> None:
        """Returns the current notifier status"""
        await ctx.reply(
            self._task.get_schedule() if self.is_active() else NOTIFIER_INACTIVE
        )

    @commands.command()
    @commands.has_any_role("axie", "Marketing", "Execs")
    async def notifier_manual(
        self, ctx: commands.context.Context, notify_date: str
    ) -> None:
        """(PLEASE AVOID!!) Manually invokes notifier for given day (default: current day)"""
        if self.is_active():
            self._task.schedule_notify(notify_date)
        else:
            await ctx.reply(NOTIFIER_INACTIVE)

    @commands.command()
    async def notifier_set(self, ctx: commands.context.Context) -> None:
        """
        Starts a notifier for an attached .csv CP Share Schedule
        (attach or reply to a message with an attached schedule)
        """
        # determine type of attachment
        attachments = ctx.message.attachments
        message_reference = ctx.message.reference
        if not attachments and message_reference:
            # message reply
            await self.notifier_set(message_reference)
            await ctx.message.add_reaction("✅")
        elif not attachments:
            # invalid format
            await ctx.message.add_reaction("❌")
            await ctx.reply(
                "Please attach or reply to a message with an attached schedule"
            )
        else:
            # validate and save csv attachment
            attachment = attachments[0]
            file_name = f"{SCHEDULES_DIR}/{attachment.filename}"
            if not file_name.endswith(".csv"):
                # NOTE: may need file validation to confirm csv contents
                return
            await attachment.save(file_name)

            # parse schedule and create Notifier Task
            schedule = parse_schedule(file_name)
            self._task.set_schedule(schedule)
            self._task.set_server(ctx.guild)
            self._task.set_status(True)

            await ctx.message.add_reaction("✅")

    @commands.command()
    async def notifier_disable(self, ctx: commands.context.Context) -> None:
        """Cancels the current running Notifier task"""
        if self.is_active():
            self._task.set_status(False)
        else:
            await ctx.message.add_reaction("❌")
            await ctx.reply(NOTIFIER_INACTIVE)


def setup(client: commands.bot.Bot) -> None:
    client.add_cog(CPNotifier(client))
