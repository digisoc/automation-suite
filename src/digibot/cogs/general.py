""" Module Imports """
# import discord
from discord.ext import commands


class General(commands.Cog):
    """DigiBot General Features"""

    def __init__(self, client):
        """Constructor for General Cog"""
        self._client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Method which is invokes when a member joins a guild"""
        # NOTE: requires SERVER MEMBERS INTENT
        print(member)
        await member.send("hi")
        channel = member.guild.system_channel
        await channel.send(
            f"Welcome {member.mention} to the DigiSoc Teams Discord! Please change your nickname to your actual name :smiley_cat:"
        )

    @commands.command(description="check if DigiBot is asleep")
    async def ping(self, ctx: commands.context.Context):
        """Replies to a !beep message with boop!"""
        # TODO: add round trip time
        await ctx.message.add_reaction("👋")
        await ctx.reply(content="boop!")


def setup(client):
    client.add_cog(General(client))
