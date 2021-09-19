""" Module Imports """
import discord
from discord.utils import get

""" Helper Imports """
from src.digibot.utils import debug

""" Constants """
FORM_EVENT_NAME_INDEX = 2
FORM_PORTFOLIOS_INDEX = 4


@debug
async def forward_request(message: discord.Message) -> None:
    """
    Sets up an event thread for a new request
    """
    # retrieve data
    server = message.guild
    embed = message.embeds[0]
    event_name = embed.fields[FORM_EVENT_NAME_INDEX].value
    channel_name = "-".join(event_name.split())

    # extract relevant portfolios
    roles = ["Execs", "Marketing", "Digital", "axie"]
    portfolios_field = embed.fields[FORM_PORTFOLIOS_INDEX]
    if portfolios_field.name == "Which Portfolio(s) are involved?":
        roles += portfolios_field.value.split("\n")
    # map role name to discord.Role object
    roles = [get(server.roles, name=role) for role in roles]

    # setup permissions for roles (view channel)
    permissions = {
        role: discord.PermissionOverwrite(read_messages=True) for role in roles
    }
    # default permissions (unable to view channel)
    permissions[server.default_role] = discord.PermissionOverwrite(read_messages=False)
    # execs permissions (manage permissions)
    permissions[roles[0]] = discord.PermissionOverwrite(
        read_messages=True, manage_permissions=True
    )
    # DigiBot permissions (view channel)
    permissions[server.me] = discord.PermissionOverwrite(read_messages=True)

    # create new channel under events category
    category = get(server.categories, name="🍺-Events")
    new_channel = await category.create_text_channel(
        name=channel_name,
        overwrites=permissions,
        topic="Ask execs to invite extra members if required | !archive to destroy channel (execs only)",
    )

    # forward google forms to discord notification embed and created forms
    form_details = message.content
    status = (
        f"A new channel has been automatically set up for {event_name}!\n{form_details}"
    )
    forwarded_message = await new_channel.send(content=status, embed=embed)
    await forwarded_message.pin()

    print(status)
