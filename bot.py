import os
from dotenv import load_dotenv
import discord
from discord.utils import get
from app import start_server

load_dotenv()
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} online')


@client.event
async def on_message(message):
    # respond to messages from the #request channel
    if message.channel.name != 'requests':
        return

    # retrieve data
    server = message.guild
    embed = message.embeds[0]

    portfolio = embed.fields[2].value
    event_name = '-'.join(embed.fields[4].value.split())

    # setup permissions
    roles = ['Execs', 'Marketing', 'Digital', 'axie'] + [portfolio]
    roles = [role for role in server.roles if role.name in roles]
    permissions = {role: discord.PermissionOverwrite(read_messages=True) for role in roles}
    permissions[server.default_role] = discord.PermissionOverwrite(read_messages=False)
    permissions[server.me] = discord.PermissionOverwrite(read_messages=True)

    # create new channel
    category = get(server.categories, name='🍺-Events')
    new_channel = await category.create_text_channel(name=event_name, overwrites=permissions)

    # forward google forms to discord notification embed
    status = f'A new channel has been automatically setup for {embed.fields[4].value}!'
    await new_channel.send(content=status, embed=embed)
    print(status)


if __name__ == '__main__':
    start_server()
    client.run(os.getenv('TOKEN'))
