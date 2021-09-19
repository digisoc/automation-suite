""" Module Imports """
import discord
from discord.ext import commands


class Misc(commands.Cog):
    """DigiBot General Features"""

    def __init__(self, client: commands.bot.Bot) -> None:
        """Constructor for Misc Cog"""
        self._client: commands.bot.Bot = client

    @commands.command()
    async def best_portfolio(self, ctx: commands.context.Context) -> None:
        """What is the best portfolio?"""
        await ctx.reply(content="IT!")

    @commands.command()
    async def axie(self, ctx: commands.context.Context) -> None:
        """Shameless plug"""
        await ctx.reply("https://github.com/axieax/")


def setup(client: commands.bot.Bot) -> None:
    client.add_cog(Misc(client))
