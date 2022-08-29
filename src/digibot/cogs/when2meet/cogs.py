""" Module Imports """
import json
import os

import discord
from discord.ext import commands

complete = ['asha', 'ryan']
GREETINGS = ("Howdy", "Ni Hao", "Hola", "Bonjour", "Ciao", "Konichiwa", "Ola")

class When2Meet(commands.Cog):
    """When2Meet Notifier"""
    def __init__(self, client: commands.Bot) -> None:
        self._client: commands.Bot = client
    
    def _get_servers(self) -> Dict[int, discord.Guild]:
        """
        Gets all the servers the bot is in

        Returns:
            servers (dict): maps guild id (int) -> guild objects (discord.Guild)
        """
        guilds = self._client.guilds
        servers = {}
        for guild in guilds:
            servers[guild.id] = guild
        return servers

    @commands.command()
    async def when2meet(self, ctx: commands.Context, url, frequency, *members) -> None:
        """Reminds members who haven't responded to a when2meet to do so"""
        await ctx.message.add_reaction("✅")
        members = list(members)
        incomplete = list(set(members) - set(complete))
        servers = self._get_servers()
        
        # send dm to incomplete members
        for user in incomplete:
            message = "please fill form at " + url + " and respond to the poll"
            embed = discord.Embed(title="When2Meet", description=message, color=0x00ff00)
            
            
    
def setup(client: commands.Bot) -> None:
    client.add_cog(When2Meet(client))
