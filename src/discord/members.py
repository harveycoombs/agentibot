from discord.api import DiscordAPI

class Members:
    @staticmethod
    async def get_members(guild_id):
        try:
            members = await DiscordAPI.get(f"guilds/{guild_id}/members")
            return members
        except Exception:
            raise Exception(":bangbang: Unable to retrieve members.")
        
    @staticmethod
    async def get_member(guild_id, user_id):
        try:
            member = await DiscordAPI.get(f"guilds/{guild_id}/members/{user_id}")
            return member
        except Exception:
            raise Exception(":bangbang: Unable to retrieve member.")
    
    @staticmethod
    async def update_member(guild_id, user_id, nickname):
        try:
            await DiscordAPI.patch(f"guilds/{guild_id}/members/{user_id}", {
                "nick": nickname
            })
        except Exception:
            raise Exception(":bangbang: Unable to update member.")
    
    @staticmethod
    async def remove_member(guild_id, user_id):
        try:
            await DiscordAPI.delete(f"guilds/{guild_id}/members/{user_id}")
        except Exception:
            raise Exception(":bangbang: Unable to remove member.")

    @staticmethod
    async def ban_member(guild_id, user_id, reason):
        try:
            await DiscordAPI.post(f"guilds/{guild_id}/bans/{user_id}", {
                "reason": reason
            })
        except Exception:
            raise Exception(":bangbang: Unable to ban member.")

    @staticmethod
    async def unban_member(guild_id, user_id):
        try:
            await DiscordAPI.delete(f"guilds/{guild_id}/bans/{user_id}")
        except Exception:
            raise Exception(":bangbang: Unable to unban member.")