from utils.api import DiscordAPI

class Guilds:
    @staticmethod
    async def get_guilds():
        guilds = await DiscordAPI.get("users/@me/guilds")
        return guilds

    @staticmethod
    async def get_guild(guild_id):
        guild = await DiscordAPI.get(f"guilds/{guild_id}?with_counts=true")
        return guild

    @staticmethod
    async def update_guild(guild_id, params):
        await DiscordAPI.patch(f"guilds/{guild_id}", params)

    @staticmethod
    async def leave_guild(guild_id):
        await DiscordAPI.delete(f"users/@me/guilds/{guild_id}")