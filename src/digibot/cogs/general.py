""" Module Imports """
import discord
from discord.ext import commands


class General(commands.Cog):
    """DigiBot General Features"""

    def __init__(self, client: commands.bot.Bot) -> None:
        """Constructor for General Cog"""
        self._client: commands.bot.Bot = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.member.Member) -> None:
        """Method which is invokes when a member joins a guild"""
        # NOTE: requires SERVER MEMBERS INTENT
        channel = member.guild.system_channel
        await channel.send(
            f"Welcome {member.mention} to the DigiSoc Teams Discord! Please change your nickname to your actual name :smiley_cat:"
        )

    @commands.command()
    async def beep(self, ctx: commands.context.Context):
        """Check if DigiBot is asleep"""
        # TODO: add round trip time
        await ctx.message.add_reaction("👋")
        await ctx.reply(content="boop!")


def setup(client: commands.bot.Bot) -> None:
    client.add_cog(General(client))
