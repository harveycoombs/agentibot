from discord.api import DiscordAPI

class Members:
    @staticmethod
    async def get_members(guild_id):
        members = await DiscordAPI.get(f"guilds/{guild_id}/members")
        return members
        
    @staticmethod
    async def get_member(guild_id, user_id):
        member = await DiscordAPI.get(f"guilds/{guild_id}/members/{user_id}")
        return member
    
    @staticmethod
    async def update_member(guild_id, user_id, nickname):
        await DiscordAPI.patch(f"guilds/{guild_id}/members/{user_id}", {
            "nick": nickname
        })