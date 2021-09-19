""" Module Imports """
import discord
from discord.ext import commands

""" Helper Imports """
from src.digibot.cogs.event_thread.setup import forward_request
from src.digibot.cogs.event_thread.destroy import archive_channel

""" Constants """
REQUESTS_CHANNEL = "requests"


class EventThread(commands.Cog):
    """DigiBot Event Thread Features"""

    def __init__(self, client):
        """Constructor for Event Thread Cog"""
        self._client = client

    def _is_from_requests_channel(self, ctx: commands.context.Context) -> bool:
        """Checks if an incoming message originates from the requests channel"""
        return ctx.channel.name == REQUESTS_CHANNEL

    def _is_webhook_request(self, ctx: commands.context.Context) -> bool:
        return ctx.author.bot and not (ctx.author == self._client.user)

    @commands.Cog.listener()
    async def on_message(self, ctx: commands.context.Context) -> None:
        # check channel
        if not self._is_from_requests_channel(ctx):
            return
        # check webhook request
        if not self._is_webhook_request(ctx):
            return
        # create event thread
        await forward_request(ctx)
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def redo(self, ctx: commands.context.Context) -> None:
        # check channel
        if not self._is_from_requests_channel(ctx):
            await ctx.message.add_reaction("❌")
            await ctx.reply(
                "Redo command must be invoked from the #requests text channel"
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
        print("after")
        await ctx.message.add_reaction("✅")

    @commands.command(description="archives and destroys an event thread")
    @commands.has_any_role("Execs", "axie")
    async def archive(self, ctx: commands.context.Context) -> None:
        """Archives a Discord text channel"""
        # check permissions
        await archive_channel(ctx)


def setup(client):
    client.add_cog(EventThread(client))
