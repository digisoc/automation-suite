""" Module Imports """
import os
import discord
from discord.utils import get

""" Archives Directory """
ARCHIVES_DIR = "./archives"
if not os.path.exists(ARCHIVES_DIR):
    os.mkdir(ARCHIVES_DIR)


async def archive_channel_content(channel: discord.TextChannel) -> str:
    """
    Extracts and returns channel history as a string
    """
    messages = await channel.history().flatten()
    history_string = channel.name + "\n"
    # traverse messages in reverse
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


async def archive_channel(message: discord.Message) -> None:
    """
    Archives a text channel
    """
    # extract channel content
    channel = message.channel
    channel_content = await archive_channel_content(channel)

    # save to file (WARNING: this may be insecure)
    file_name = f"{ARCHIVES_DIR}/{channel.name}.txt"
    with open(file_name, "w") as f:
        f.write(channel_content)

    # post archive file to archives channel
    archive_channel = get(message.guild.channels, name="archives")
    status = f"Archive successfully generated for {channel.name}"
    await archive_channel.send(content=status, file=discord.File(file_name))
    print(status)

    # delete event channel
    await channel.delete(reason="Archived (please check #archives)")
