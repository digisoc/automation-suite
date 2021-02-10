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


async def archive_channel_content(channel):
    '''
    Extracts and returns channel history as a string
    '''
    messages = await channel.history().flatten()
    history_string = channel.name + '\n'
    for message in messages[::-1]:
        # extract message info
        history_string += f'\n{message.author} {message.created_at}'
        history_string += f'\n{message.clean_content}'
        # extract message attachments (files and images)
        if message.attachments:
            history_string += f'\nAttachments:'
            for attachment in message.attachments:
                history_string += f'\n\t{attachment.url}'
        # extract message embeds
        if message.embeds:
            history_string += f'\nEmbeds:'
            for embed in message.embeds:
                history_string += f'\n{embed.title}'
            for field in embed.fields:
                history_string += f'\n{field.name}'
                history_string += f'\n{field.value}\n'
        history_string += '\n'
    return history_string


async def push_request(message):
    '''
    Sets up a new channel for new requests
    '''
    # retrieve data
    server = message.guild
    embed = message.embeds[0]

    portfolio = embed.fields[2].value
    event_name = '-'.join(embed.fields[4].value.split())

    # setup permissions for roles (execs able to manage permissions)
    roles = ['Execs', 'Marketing', 'Digital', 'axie'] + [portfolio]
    roles = [get(server.roles, name=role) for role in roles]

    permissions = {role: discord.PermissionOverwrite(read_messages=True) for role in roles}
    permissions[roles[0]] = discord.PermissionOverwrite(manage_permissions=True)
    permissions[server.default_role] = discord.PermissionOverwrite(read_messages=False)
    permissions[server.me] = discord.PermissionOverwrite(read_messages=True)

    # create new channel under events category
    category = get(server.categories, name='🍺-Events')
    new_channel = await category.create_text_channel(
        name=event_name,
        overwrites=permissions,
        topic='Ask execs to invite extra members if required | !archive to destroy channel (execs only)',
    )

    # forward google forms to discord notification embed
    status = f'A new channel has been automatically setup for {embed.fields[4].value}!'
    await new_channel.send(content=status, embed=embed)
    print(status)


@client.event
async def on_message(message):
    # respond to messages from the #request channel
    channel = message.channel
    user_roles = [role.name for role in message.author.roles]
    if channel.name == 'requests':
        # redo push request for referenced message
        if message.content == '!redo' and message.reference:
            await push_request(message.reference.resolved)
            await message.add_reaction('✅')
        # push request to new channel
        elif message.author.bot and message.author != client.user:
            await push_request(message)
            await message.add_reaction('✅')
    elif message.content == '!archive' and 'Execs' in user_roles:
        # extract channel content
        content = await archive_channel_content(channel)
        # write to file
        file_name = f'./archives/{channel.name}'
        if not os.path.exists('./archives'):
            os.makedirs('./archives')
        with open(file_name, 'w') as f:
            f.write(content)
        # post file to #requests
        requests_channel = get(message.guild.channels, name='requests')
        status = f'Archive successfully generated for {channel.name}'
        with open(file_name, 'r') as f:
            await requests_channel.send(content=status, file=discord.File(f, filename=f'{channel.name}-archive.txt'))
        print(status)
        # delete event channel
        channel.delete(reason='Archived (check #requests)')
        print('Channel deleted')


if __name__ == '__main__':
    start_server()
    client.run(os.getenv('TOKEN'))
