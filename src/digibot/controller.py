""" Module Imports """
import os
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

""" Constants """
COGS_DIR = "src/digibot/cogs"
ACTIVE_COGS = []


"""
Discord Bot Client
Permissions:
- Coded Intents: members (https://discordpy.readthedocs.io/en/latest/api.html#discord.Intents.members)
- Privileged Intents: Server Members Intent, Message Content Intent (enable through GUI)
- Bot Permissions (DigiBot Role): Administrator
"""
command_prefix = "!"
activity = discord.Activity(type=discord.ActivityType.playing, name="beep boop!")

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=command_prefix, intents=intents, activity=activity)


# TODO: convert to Discord slash commands
# TODO: attach logger (who activated what command)
# TODO: more consistent command reactions
# TODO: setup black formatter pipeline


@client.event
async def on_ready() -> None:
    """
    Async function which is activated when DigiBot becomes online
    """
    print(f"{client.user} online")
    load_cogs()
    print(f"Active Cogs: {ACTIVE_COGS}")


""" COGS (extensions) """


@client.command(
    name="reload",
    aliases=["restart", "refresh"],
)
async def reload_cogs(ctx: commands.Context) -> None:
    """Hot refreshes DigiBot"""
    unload_cogs()
    load_cogs()
    await ctx.message.add_reaction("✅")
    print("Cogs successfully reloaded!")


def load_cogs() -> None:
    """Loads Discord Cogs"""
    for file in os.scandir(COGS_DIR):
        # traverses each file/dir in the COGS directory
        name = file.name
        # ignore __*, e.g. __init__.py
        if name.startswith("__"):
            continue
        # strip .py extension
        if file.is_file():
            name = name.strip(".py")
        # load cog
        cog_name = f"{COGS_DIR}/{name}".replace("/", ".")
        client.load_extension(cog_name)
        ACTIVE_COGS.append(cog_name)


def unload_cogs() -> None:
    """Unloads Discord Cogs"""
    for cog_name in ACTIVE_COGS:
        client.unload_extension(cog_name)
    ACTIVE_COGS.clear()


async def start_discord_server() -> None:
    """Starts up DigiBot"""
    # get TOKEN environment variable
    load_dotenv()
    token = os.getenv("TOKEN")
    if not token:
        print("ERROR: no Discord bot token found", file=sys.stderr)
        exit(1)
    # start Discord client
    await client.start(token)
