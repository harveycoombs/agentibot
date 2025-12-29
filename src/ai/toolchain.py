import json

from discord.roles import Roles
from discord.members import Members
from discord.channels import Channels
from discord.messages import Messages
from discord.permissions import Permissions
from discord.guilds import Guilds
from exception import VesperException
 
def get_bot_creator() -> str:
    """Gets the creator of you, the bot."""
    return "[Harvey Coombs](https://harveycoombs.com)"

async def get_server_info(guild_id: str) -> str:
    """Gets information about the current server."""
    guild = await Guilds.get_guild(guild_id)
    return json.dumps(guild)

async def add_role(role_name: str, guild_id: str, author_id: str, target_id: str = None) -> str:
    """Adds a role to another user. Input should be a string with the role's name."""
    roles = await Roles.get_roles(guild_id)
    role = next((role for role in roles if role["name"].lower() == role_name.lower()), None)

    if role is None:
        raise VesperException(":warning: The provided role does not exist.")
    
    await Roles.add_role_to_user(guild_id, author_id if target_id is None else target_id, role["id"])
    return f":white_check_mark: I have added the '{role_name}' role."

async def remove_role(role_name: str, guild_id: str, author_id: str, target_id: str = None) -> str:
    """Removes a role from another user. Input should be a string with the role's name."""
    roles = await Roles.get_roles(guild_id)
    role = None

    try:
        role = next((role for role in roles if role["name"].lower() == role_name.lower()), None)
    except:
        role = None

    if role is None:
        raise VesperException(f":warning: The provided role does not exist.")
    
    await Roles.remove_role_from_user(guild_id, author_id if target_id is None else target_id, role["id"])
    return f":white_check_mark: I have removed the '{role_name}' role."

async def create_role(role_name: str, role_color: str, guild_id: str, author_id: str) -> str:
    """Creates a role. Input should be a string with the role's name and a string with the role's color."""
    color_hex = role_color.replace("#", "").replace("\"", "").strip()
    safe_role_name = role_name.strip("\"").strip()

    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise VesperException(":no_entry_sign: You do not have permission to create roles.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_ROLES) or guild["owner_id"] == author_id:
            break
        else:
            raise VesperException(":no_entry_sign: You do not have permission to create roles.")

    await Roles.create_role(guild_id, safe_role_name, int(color_hex, 16))
    return f":white_check_mark: I have created the '{safe_role_name}' role."

async def change_nickname(nickname: str, guild_id: str, author_id: str) -> str:
    """Changes the nickname of a user. Input should be a string with the new nickname."""
    await Members.update_member(guild_id, author_id, nickname)
    return f":white_check_mark: I have changed your nickname to '{nickname}'."

async def create_text_channel(channel_name: str, guild_id: str, message_author_id: str, category_name: str = None) -> str:
    """Creates a text channel. Input should be a string with the channel's name and optionally a string with the category's name."""
    print(channel_name, guild_id, message_author_id, category_name)

    member = await Members.get_member(guild_id, message_author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != message_author_id:
        raise VesperException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == message_author_id:
            break
        else:
            raise VesperException(":no_entry_sign: You do not have permission to create channels.")

    new_channel_id = await Channels.create_channel(guild_id, channel_name, 0, category_name)
    return f":white_check_mark: I have created the <#{new_channel_id}> channel."

async def create_voice_channel(channel_name: str, guild_id: str, message_author_id: str, category_name: str = None) -> str:
    """Creates a voice channel. Input should be a string with the channel's name and optionally a string with the category's name."""
    member = await Members.get_member(guild_id, message_author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != message_author_id:
        raise VesperException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == message_author_id:
            break
        else:
            raise VesperException(":no_entry_sign: You do not have permission to create channels.")
        
    new_channel_id = await Channels.create_channel(guild_id, channel_name, 2, category_name)
    return f":white_check_mark: I have created the <#{new_channel_id}> channel."

async def delete_channel(channel_name: str, guild_id: str, author_id: str) -> str:
    """Deletes a channel. Input should be a string with the channel's name."""
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise VesperException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == author_id:
            break
        else:
            raise VesperException(":no_entry_sign: You do not have permission to delete channels.")
        
    channels = await Channels.get_channels(guild_id)
    channel = next((channel for channel in channels if channel["name"].strip().lower() == channel_name.strip().lower()), None)

    if channel is None:
        raise VesperException(f":warning: The provided channel does not exist.")

    await Channels.delete_channel(channel["id"])
    return f":white_check_mark: I have deleted the '{channel_name}' channel."

async def rename_channel(guild_id: str, channel_name: str, new_name: str, message_author_id: str) -> str:
    """Renames a channel. Input should be a string with the channel's name and a string with the new name."""

    print("renaming channel...")

    member = await Members.get_member(guild_id, message_author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != message_author_id:
        raise VesperException(":no_entry_sign: You do not have permission to rename channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == message_author_id:
            break
        else:
            raise VesperException(":no_entry_sign: You do not have permission to rename channels.")

    channels = await Channels.get_channels(guild_id)
    channel = next((channel for channel in channels if channel["name"].strip().lower() == channel_name.strip().lower()), None)

    if channel is None:
        raise VesperException(f":warning: The provided channel does not exist.")

    await Channels.rename_channel(channel["id"], new_name)
    return f":white_check_mark: I have renamed the <#{channel['id']}> channel to '{new_name}'."

async def delete_message(channel_id: str, message_id: str, guild_id: str, author_id: str) -> str:
    """Deletes a message. Input should be a string with the message's ID.""" 
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise VesperException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_MESSAGES) or guild["owner_id"] == author_id:
            break
        else:
            raise VesperException(":no_entry_sign: You do not have permission to delete messages.")
        
    await Messages.delete_message(channel_id, message_id)
    return ":white_check_mark: I have deleted the referenced message."

async def bulk_delete_messages(amount: int, channel_id: str, guild_id: str, author_id: str) -> str:
    """Bulk deletes messages in the current channel. Input should be a number with the amount of messages to delete."""
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise VesperException(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_MESSAGES) or guild["owner_id"] == author_id:
            break
        else:
            raise VesperException(":no_entry_sign: You do not have permission to delete messages.")
        
    await Messages.bulk_delete_messages(channel_id, amount)
    return f":white_check_mark: I have deleted {amount} messages."

async def ban_member(member_id: str, reason: str, guild_id: str, author_id: str) -> str:
    """Bans a member. Input should be a string with the reason for the ban."""
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise VesperException(":no_entry_sign: You do not have permission to ban members.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.BAN_MEMBERS) or guild["owner_id"] == author_id:
            break
        else:
            raise VesperException(":no_entry_sign: You do not have permission to ban members.")
        
    await Members.ban_member(guild_id, member_id, reason)
    return f":white_check_mark: I have banned <@{member_id}>."

async def unban_member(member_id, guild_id, author_id):
    """Unbans a member. Input should be a string with the member's ID."""
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise VesperException(":no_entry_sign: You do not have permission to unban members.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.BAN_MEMBERS) or guild["owner_id"] == author_id:
            break
    await Members.unban_member(guild_id, member_id)
    return f":white_check_mark: I have unbanned <@{member_id}>."

async def kick_member(member_id: str, guild_id: str, author_id: str) -> str:
    """Kicks a member. Input should be a string with the member's ID."""
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise VesperException(":no_entry_sign: You do not have permission to kick members.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.KICK_MEMBERS) or guild["owner_id"] == author_id:
            break
        else:
            raise VesperException(":no_entry_sign: You do not have permission to kick members.")
        
    await Members.remove_member(guild_id, member_id)
    return f":white_check_mark: I have kicked <@{member_id}>."