""" Module Imports """
import os

import discord
from discord.ext import commands
from discord.utils import get

""" Constants """
ARCHIVES_DIR = "src/digibot/cogs/event_thread/archives"
if not os.path.exists(ARCHIVES_DIR):
    os.mkdir(ARCHIVES_DIR)


async def archive_channel_content(channel: discord.TextChannel) -> str:
    """
    Extracts and returns channel history as a string
    """
    messages = await channel.history().flatten()
    history_string = channel.name + "\n"
    # traverse messages in reverse order
    for message in messages[::-1]:
        # extract message info
        history_string += (
            f"\n{message.author} {message.created_at}\n{message.clean_content}"
        )

        # extract message attachments (files and images)
        if message.attachments:
            history_string += f"\nAttachments:" + "\n\t".join(
                attachment.url for attachment in message.attachments
            )

        # extract message embeds
        if message.embeds:
            history_string += f"\nEmbeds:"
            for embed in message.embeds:
                history_string += f"\n{embed.title}"
                for field in embed.fields:
                    history_string += f"\n{field.name}"
                    history_string += f"\n{field.value}\n"
        history_string += "\n"

    return history_string


def generate_archive_file(channel_name: str, channel_content: str) -> discord.File:
    """
    Creates a local file for the archived channel content
    and returns a discord.File object for it
    """
    # save to file (WARNING: strcat may be insecure)
    file_name = f"{ARCHIVES_DIR}/{channel_name}.txt"
    with open(file_name, "w") as f:
        f.write(channel_content)

    return discord.File(file_name)


async def archive_channel(ctx: commands.Context) -> None:
    """
    Archives a text channel
    """
    # get channel information
    channel = ctx.channel
    archive_channel = get(ctx.guild.channels, name="archives")

    # no archive channel found
    if not archive_channel:
        await ctx.message.add_reaction("❌")
        await ctx.reply("No #archives text channel found!")

    else:
        # extract channel content
        channel_content = await archive_channel_content(channel)
        archive_file = generate_archive_file(channel.name, channel_content)

        if channel == archive_channel:
            # requested archive on archives channel
            await ctx.message.add_reaction("❓")
            await ctx.author.send(
                "Beep boop, here are your archives! :robot:", file=archive_file
            )
            await ctx.reply(
                "Can't archive the archives channel, but a copy of this channel has been sent to your DM's!"
            )
        else:
            # post archive file to archives channel
            status = f"Archive successfully generated for {channel.name}"
            await archive_channel.send(content=status, file=archive_file)
            print(status)

            # delete event channel
            await channel.delete(reason="Archived (please check #archives)")
