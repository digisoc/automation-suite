""" Module Imports """
import discord
from discord.ext import commands


class General(commands.Cog):
    """DigiBot General Features"""

    def __init__(self, client: commands.Bot) -> None:
        """Constructor for General Cog"""
        self._client: commands.Bot = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """Method which is invokes when a member joins a guild"""
        channel = member.guild.system_channel
        await channel.send(
            f"Welcome {member.mention} to the DigiSoc Team Discord! Please change your nickname to your actual name :smiley_cat:"
        )

    @commands.command()
    async def beep(self, ctx: commands.Context) -> None:
        """Check if DigiBot is asleep"""
        # TODO: add round trip time
        await ctx.message.add_reaction("👋")
        await ctx.reply(content="shutup!")

    @commands.command()
    async def echo(self, ctx: commands.Context, *args) -> None:
        """Plagiarism without the academic integrity"""
        await ctx.message.add_reaction("✅")
        await ctx.channel.send(" ".join(args))


def setup(client: commands.Bot) -> None:
    client.add_cog(General(client))
