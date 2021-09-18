""" Module Imports """
import os
import discord
from dotenv import load_dotenv

""" Import DigiBot Features """
from src.digibot.features.general import ping
from src.digibot.features.event_thread.setup import forward_request
from src.digibot.features.event_thread.destroy import archive_channel

""" Constants """
CAN_ARCHIVE_ROLES = {"Execs", "axie"}


""" Discord Bot Client """
client = discord.Client()
default_prefix = "!"


@client.event
async def on_ready() -> None:
    """
    Async function which is activated when DigiBot becomes online
    """
    print(f"{client.user} online")


@client.event
async def on_message(message: discord.Message) -> None:
    """
    Async function which is activated for all new messages sent and visible to DigiBot
    """
    # TODO: python3.10 match-case can be used here
    try:
        # retrieve message information
        author = message.author
        is_author_bot = message.author.bot
        channel = message.channel
        message_content = message.content

        # get roles for non-bot user
        user_roles = (
            {role.name for role in author.roles} if not is_author_bot else set()
        )
        can_user_archive = bool(CAN_ARCHIVE_ROLES.intersection(user_roles))

        # general ping command
        if message_content == default_prefix + "beep":
            await ping(channel)
            return

        # automation commands
        if channel.name == "requests":
            is_digibot = author == client.user
            if message.content == default_prefix + "redo" and (
                message_reference := message.reference
            ):
                # redo push request for referenced message
                await forward_request(message_reference.resolved)
                await message.add_reaction("✅")
                return
            # push request to new channel
            elif is_author_bot and not is_digibot:
                # webhook request
                await forward_request(message)
                await message.add_reaction("✅")
                return

        # normal channel
        elif message_content == default_prefix + "archive" and can_user_archive:
            await archive_channel(message)
            return

    except Exception as e:
        print(e)
        await message.channel.send(e)


def start_discord_server() -> None:
    """Starts up DigiBot"""
    # get TOKEN environment variable
    load_dotenv()
    token = os.getenv("TOKEN")
    # start Discord client
    client.run(token)


if __name__ == "__main__":
    start_discord_server()
