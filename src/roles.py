from utils.api import DiscordAPI

class Roles:
    @staticmethod
    async def get_roles(guild_id):
        roles = await DiscordAPI.get(f"guilds/{guild_id}/roles")
        return roles

    @staticmethod
    async def get_role(guild_id, role_id):
        role = await DiscordAPI.get(f"guilds/{guild_id}/roles/{role_id}")
        return role
    
    @staticmethod
    async def create_role(guild_id, name, color=0, hoist=False, mentionable=False, permissions=[]):
        await DiscordAPI.post(f"guilds/{guild_id}/roles", {
            "name": name,
            "color": color,
            "hoist": hoist,
            "mentionable": mentionable,
            "permissions": permissions
        })
        
    @staticmethod
    async def delete_role(guild_id, role_id):
        await DiscordAPI.delete(f"guilds/{guild_id}/roles/{role_id}")

    @staticmethod
    async def add_role_to_user(guild_id, user_id, role_id):
        await DiscordAPI.put(f"guilds/{guild_id}/members/{user_id}/roles/{role_id}", payload=None)

    @staticmethod
    async def remove_role_from_user(guild_id, user_id, role_id):
        await DiscordAPI.delete(f"guilds/{guild_id}/members/{user_id}/roles/{role_id}")