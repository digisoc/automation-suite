""" Module Imports """
import os

import discord
from discord.ext import commands

""" Helper Imports """
from src.digibot.cogs.cp_share_notify.helpers import (SCHEDULE_TYPE,
                                                      parse_schedule)
from src.digibot.cogs.cp_share_notify.task import CPTask

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
            embed = await self._create_embed(self._task.get_schedule())
            await ctx.send(embed=embed)
        else:
            await ctx.message.add_reaction("❓")
            await ctx.reply(NOTIFIER_INACTIVE)

    async def _create_embed(self, schedule: SCHEDULE_TYPE) -> discord.Embed:
        """Creates am embed for a given schedule"""
        # NOTE: sort by day? add current csv file name to description?
        # create discord.Embed object
        embed = discord.Embed(
            title="CP Share Notifier",
            description="Status: Enabled :green_circle:",
            color=10511870,
        )

        # set image as DigiBot logo
        avatar = self._client.user.avatar_url
        embed.set_thumbnail(url=str(avatar))

        # add fields
        for day, users in schedule.items():
            users_info = (
                f"**{user['name']}:** {user['event']} ({user['share_type']})"
                for user in users
            )
            embed.add_field(name=day, value="\n".join(users_info))

        embed.set_footer(text="DigiBot CP Share Automation - https://github.com/axieax")
        return embed

    @commands.command()
    @commands.has_any_role("axie", "Execs")
    async def notifier_manual(
        self, ctx: commands.Context, notify_date: str = ""
    ) -> None:
        """(PLEASE AVOID!!) Manually invokes notifier for given day (default: current day)"""
        if self.is_active():
            await self._task.schedule_notify_async(notify_date)
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
        is_success = False
        message_reference = ctx.message.reference
        if message_reference:
            is_success = await self._notifier_set(message_reference.resolved, ctx.guild)
        else:
            is_success = await self._notifier_set(ctx.message, ctx.guild)

        await ctx.message.add_reaction("✅" if is_success else "❌")

    async def _notifier_set(
        self, message: discord.Message, server: discord.Guild
    ) -> bool:
        """
        Extract and parse .csv CPShare Schedule file in given message

        Return:
            success_status (bool)
        """
        if not message.attachments:
            # message does not contain any attachments
            return False

        # validate and save csv attachment
        attachment = message.attachments[0]
        file_name = f"{SCHEDULES_DIR}/{attachment.filename}"
        if not file_name.endswith(".csv"):
            # NOTE: may need file validation to confirm csv contents
            return False
        await attachment.save(file_name)

        # parse schedule and create Notifier Task
        try:
            schedule = parse_schedule(file_name)
            self._task.set_schedule(schedule)
            self._task.set_server(server)
            self._task.set_status(True)
        except Exception as e:
            print(e)
            # raise
            return False

        return True

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
