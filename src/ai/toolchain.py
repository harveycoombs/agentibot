from discord.roles import Roles
from discord.members import Members
from discord.channels import Channels
from discord.messages import Messages

async def add_role(role_name, guild_id, author_id):
    roles = await Roles.get_roles(guild_id)
    role = next((role for role in roles if role["name"].lower() == role_name.lower()), None)

    if role is None:
        return ":warning: Sorry, I couldn't find that role."
    
    await Roles.add_role_to_user(guild_id, author_id, role["id"])
    return ":white_check_mark: I have added that role to you."

async def remove_role(role_name, guild_id, author_id):
    roles = await Roles.get_roles(guild_id)
    role = next((role for role in roles if role["name"].lower() == role_name.lower()), None)

    if role is None:
        return f":warning: Sorry, I couldn't find the '{role_name}' role."
    
    await Roles.remove_role_from_user(guild_id, author_id, role["id"])
    return f":white_check_mark: I have removed the '{role_name}' role from you."

async def change_nickname(nickname, guild_id, author_id):
    await Members.update_member(guild_id, author_id, nickname)
    return f":white_check_mark: I have changed your nickname to '{nickname}'."

async def create_text_channel(channel_name, guild_id):
    new_channel_id = await Channels.create_channel(guild_id, channel_name)
    return f":white_check_mark: I have created the <#{new_channel_id}> channel."

async def create_voice_channel(channel_name, guild_id):
    new_channel_id = await Channels.create_channel(guild_id, channel_name, 2)
    return f":white_check_mark: I have created the <#{new_channel_id}> channel."

async def delete_channel(target_channel_id):
    await Channels.delete_channel(target_channel_id)
    return f":white_check_mark: I have deleted the <#{target_channel_id}> channel."

async def delete_message(channel_id, event_data):
    referenced_message_id = event_data["referenced_message"]["id"] if "referenced_message" in event_data else None
    
    if referenced_message_id is None:
        return ":warning: No message to delete."
        
    await Messages.delete_message(channel_id, referenced_message_id)
    return ":white_check_mark: I have deleted the referenced message."

async def ban_member(member_id, guild_id):
    await Members.ban_member(guild_id, member_id)
    return f":white_check_mark: I have banned <@{member_id}>."

async def unban_member(member_id, guild_id):
    await Members.unban_member(guild_id, member_id)
    return f":white_check_mark: I have unbanned <@{member_id}>."