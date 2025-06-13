from discord.roles import Roles
from discord.members import Members
from discord.channels import Channels
from discord.messages import Messages
from discord.permissions import Permissions
from discord.guilds import Guilds
 
def get_bot_creator():
    return "[Harvey Coombs](https://harveycoombs.com)"

async def add_role(role_name, guild_id, author_id, target_id=None):
    roles = await Roles.get_roles(guild_id)
    role = next((role for role in roles if role["name"].lower() == role_name.lower()), None)

    if role is None:
        raise Exception(":warning: The provided role does not exist.")
    
    await Roles.add_role_to_user(guild_id, author_id if target_id is None else target_id, role["id"])
    return f":white_check_mark: I have added the '{role_name}' role."

async def remove_role(role_name, guild_id, author_id, target_id=None):
    roles = await Roles.get_roles(guild_id)
    role = next((role for role in roles if role["name"].lower() == role_name.lower()), None)

    if role is None:
        raise Exception(f":warning: The provided role does not exist.")
    
    await Roles.remove_role_from_user(guild_id, author_id if target_id is None else target_id, role["id"])
    return f":white_check_mark: I have removed the '{role_name}' role."

async def create_role(role_name, role_color, guild_id, author_id):
    color_hex = role_color.replace("#", "").replace("\"", "").strip()
    safe_role_name = role_name.strip("\"").strip()

    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise Exception(":no_entry_sign: You do not have permission to create roles.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_ROLES) or guild["owner_id"] == author_id:
            break
        else:
            raise Exception(":no_entry_sign: You do not have permission to create roles.")

    await Roles.create_role(guild_id, safe_role_name, int(color_hex, 16))
    return f":white_check_mark: I have created the '{safe_role_name}' role."

async def change_nickname(nickname, guild_id, author_id):
    await Members.update_member(guild_id, author_id, nickname)
    return f":white_check_mark: I have changed your nickname to '{nickname}'."

async def create_text_channel(channel_name, guild_id, author_id):
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise Exception(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == author_id:
            break
        else:
            raise Exception(":no_entry_sign: You do not have permission to create channels.")

    new_channel_id = await Channels.create_channel(guild_id, channel_name)
    return f":white_check_mark: I have created the <#{new_channel_id}> channel."

async def create_voice_channel(channel_name, guild_id, author_id):
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise Exception(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == author_id:
            break
        else:
            raise Exception(":no_entry_sign: You do not have permission to create channels.")
        
    new_channel_id = await Channels.create_channel(guild_id, channel_name, 2)
    return f":white_check_mark: I have created the <#{new_channel_id}> channel."

async def delete_channel(target_channel_id, guild_id, author_id):
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise Exception(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == author_id:
            break
        else:
            raise Exception(":no_entry_sign: You do not have permission to delete channels.")
        
    await Channels.delete_channel(target_channel_id)
    return f":white_check_mark: I have deleted the <#{target_channel_id}> channel."

async def rename_channel(guild_id, channel_id, new_name, author_id):
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise Exception(":no_entry_sign: You do not have permission to rename channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_CHANNELS) or guild["owner_id"] == author_id:
            break
        else:
            raise Exception(":no_entry_sign: You do not have permission to rename channels.")

    await Channels.rename_channel(channel_id, new_name)

async def delete_message(channel_id, referenced_message, guild_id, author_id):
    referenced_message_id = referenced_message and referenced_message["message_id"]

    if referenced_message_id is None:
        raise Exception(":warning: There is no message to delete.")
        
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise Exception(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_MESSAGES) or guild["owner_id"] == author_id:
            break
        else:
            raise Exception(":no_entry_sign: You do not have permission to delete messages.")
        
    await Messages.delete_message(channel_id, referenced_message_id)
    return ":white_check_mark: I have deleted the referenced message."

async def bulk_delete_messages(amount, channel_id, guild_id, author_id):
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise Exception(":no_entry_sign: You do not have permission to create channels.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.MANAGE_MESSAGES) or guild["owner_id"] == author_id:
            break
        else:
            raise Exception(":no_entry_sign: You do not have permission to delete messages.")
        
    await Messages.bulk_delete_messages(channel_id, amount)
    return f":white_check_mark: I have deleted {amount} messages."

async def ban_member(member_id, reason, guild_id, author_id):
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise Exception(":no_entry_sign: You do not have permission to ban members.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.BAN_MEMBERS) or guild["owner_id"] == author_id:
            break
        else:
            raise Exception(":no_entry_sign: You do not have permission to ban members.")
        
    await Members.ban_member(guild_id, member_id, reason)
    return f":white_check_mark: I have banned <@{member_id}>."

async def unban_member(member_id, guild_id, author_id):
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise Exception(":no_entry_sign: You do not have permission to unban members.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.BAN_MEMBERS) or guild["owner_id"] == author_id:
            break
    await Members.unban_member(guild_id, member_id)
    return f":white_check_mark: I have unbanned <@{member_id}>."

async def kick_member(member_id, guild_id, author_id):
    member = await Members.get_member(guild_id, author_id)
    roles = await Roles.get_roles(guild_id)
    guild = await Guilds.get_guild(guild_id)

    member_roles = [role for role in roles if role["id"] in member["roles"]]

    if len(member_roles) == 0 and guild["owner_id"] != author_id:
        raise Exception(":no_entry_sign: You do not have permission to kick members.")

    for role in member_roles:
        if Permissions.has_permission(role["permissions_new"], Permissions.KICK_MEMBERS) or guild["owner_id"] == author_id:
            break
        else:
            raise Exception(":no_entry_sign: You do not have permission to kick members.")
        
    await Members.remove_member(guild_id, member_id)
    return f":white_check_mark: I have kicked <@{member_id}>."