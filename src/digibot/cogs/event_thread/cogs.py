""" Module Imports """
import discord
from discord.ext import commands

""" Helper Imports """
from src.digibot.cogs.event_thread.destroy import archive_channel
from src.digibot.cogs.event_thread.setup import forward_request

""" Constants """
DEV_CHANNEL = "dev"


class EventThread(commands.Cog):
    """DigiBot Event Thread Features"""

    def __init__(self, client: commands.Bot) -> None:
        """Constructor for Event Thread Cog"""
        self._client: commands.Bot = client

    def _is_from_dev_channel(self, ctx: commands.Context) -> bool:
        """Checks if an incoming message originates from the dev channel"""
        if isinstance(ctx.channel, discord.channel.TextChannel):
            return ctx.channel.name == DEV_CHANNEL
        return False  # e.g. discord.channel.DMChannel

    def _is_webhook_request(self, ctx: commands.Context) -> bool:
        """Checks if an incoming message is a Forms to Discord webhook request"""
        return ctx.author.bot and not (ctx.author == self._client.user)

    @commands.Cog.listener()
    async def on_message(self, ctx: commands.Context) -> None:
        """
        Listener for incoming Forms to Discord dev
        https://github.com/axieax/google-forms-to-discord/
        """
        # check channel
        if not self._is_from_dev_channel(ctx):
            return

        # check webhook request
        if not self._is_webhook_request(ctx):
            return

        # create event thread
        await forward_request(ctx)
        await ctx.add_reaction("✅")

    @commands.command()
    async def redo(self, ctx: commands.Context) -> None:
        """Manually creates an event thread from a referenced response"""
        # check channel
        if not self._is_from_dev_channel(ctx):
            await ctx.message.add_reaction("❌")
            await ctx.reply(
                "Redo command must be invoked from the #dev text channel"
            )
            return

        # check reference
        if not ctx.message.reference:
            await ctx.message.add_reaction("❌")
            await ctx.reply(
                "Redo command must contain a message reference (reply to a request)"
            )
            return

        # create event thread
        await forward_request(ctx.message.reference.resolved)
        await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.has_any_role("Execs", "axie")
    async def archive(self, ctx: commands.Context) -> None:
        """Archives and removes a Discord text channel"""
        # TODO: notify missing permissions?
        await archive_channel(ctx)


def setup(client: commands.Bot) -> None:
    client.add_cog(EventThread(client))
