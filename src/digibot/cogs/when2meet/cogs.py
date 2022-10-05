""" Module Imports """
import json
import os

import discord
from discord.ext import commands

complete = ['@asha', '@axieax']
GREETINGS = ("Howdy", "Ni Hao", "Hola", "Bonjour", "Ciao", "Konichiwa", "Ola")

class When2Meet(commands.Cog):
    """When2Meet Notifier"""
    def __init__(self, client: commands.Bot) -> None:
        self._client: commands.Bot = client

    @commands.command()
    async def when2meet(self, ctx: commands.Context, url, frequency, users: commands.Greedy[discord.User]) -> None:
        """Reminds members who haven't responded to a when2meet to do so"""
        await ctx.message.add_reaction("✅")
        users_names = []
        servers = self._get_servers()
        # append all server profile names to member_names
        for user in users:

            # error check
            if not user:
                print("Invalid user detected in users")
                continue

            name = user.name
            server_id = user.server_id
            server = servers.server_id
            member = server.get_member_named(name)
            users_names.append(member)
        print(users_names)
        # for member in members:
        #     try:
        #         await member.send("Hello, Wanning is testing out the new when2meet bot hahaha :)))")
        #     except:
        #         await ctx.send(f"Couldn't DM {member}.")
        # incomplete = list(set(members) - set(complete))
        # servers = self._get_servers()

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
    
def setup(client: commands.Bot) -> None:
    client.add_cog(When2Meet(client))
