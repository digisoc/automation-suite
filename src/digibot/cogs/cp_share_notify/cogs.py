""" Module Imports """
import json
import os

import discord
from discord.ext import commands

""" Helper Imports """
from src.digibot.cogs.cp_share_notify.helpers import (SCHEDULE_TYPE,
                                                      parse_schedule)
from src.digibot.cogs.cp_share_notify.task import CPTask

""" Constants """
SCHEDULE_PERSISTENCE_JSON = "schedule.json"

SCHEDULES_DIR = "src/digibot/cogs/cp_share_notify/schedules"
if not os.path.exists(SCHEDULES_DIR):
    os.mkdir(SCHEDULES_DIR)

NOTIFIER_INACTIVE = "No CPShare Schedule Notifier active :crying_cat_face:"

# cp_commands = commands.Group("cp")


class CPNotifier(commands.Cog):
    """CPShare Schedule Notifier"""

    def __init__(self, client: commands.Bot) -> None:
        self._client: commands.Bot = client
        if not os.path.exists(SCHEDULE_PERSISTENCE_JSON):
            schedule = {}
        else:
            with open(SCHEDULE_PERSISTENCE_JSON, "r") as f:
                schedule = json.load(f)
        print(f"{schedule=}")
        self._task: CPTask = CPTask(schedule, client)

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
            users_info = (f"**{user['name']}:** {user['event']}" for user in users)
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
        await self.notifier_recurse(ctx, True)

    @commands.command()
    async def notifier_add(self, ctx: commands.Context) -> None:
        """
        Adds another schedule to the current CPShare Schedule
        """
        await self.notifier_recurse(ctx, False)

    async def notifier_recurse(
        self, ctx: commands.Context, override_existing_schedule: bool
    ) -> None:
        is_success = False
        message_reference = ctx.message.reference
        if message_reference:
            is_success = await self.notifier_update(
                message_reference.resolved, ctx.guild.id, override_existing_schedule
            )
        else:
            is_success = await self.notifier_update(
                ctx.message, ctx.guild.id, override_existing_schedule
            )

        await ctx.message.add_reaction("✅" if is_success else "❌")

    async def notifier_update(
        self,
        message: discord.Message,
        server_id: int,
        override_existing_schedule: bool,
    ) -> bool:
        """
        Extract and parse .csv CPShare Schedule file in given message

        Return:
            success_status (bool)
        """
        if not message.attachments:
            # message does not contain any attachments
            await message.reply(
                "Please ensure the schedule is attached to this message"
            )
            return False

        # validate and save csv attachment
        attachment = message.attachments[0]
        file_name = f"{SCHEDULES_DIR}/{attachment.filename}"
        if not file_name.endswith(".csv"):
            # NOTE: may need file validation to confirm csv contents
            await message.reply("Please attach a valid .csv file")
            return False
        await attachment.save(file_name)

        # parse schedule and create Notifier Task
        try:
            schedule = parse_schedule(file_name, server_id)
            if override_existing_schedule:
                self._task.set_schedule(schedule)
            else:
                self._task.add_schedule(schedule)
            self._task.set_status(True)
            with open(SCHEDULE_PERSISTENCE_JSON, "w") as f:
                json.dump(schedule, f, indent=2)
        except Exception as e:
            print(e)
            # raise
            await message.reply(
                "Could not parse schedule. Please check schedule format before informing IT."
            )
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
