from discord import Message


async def ping(message: Message):
    """Replies to a !beep message with boop!"""
    await message.reply(content="boop!")
