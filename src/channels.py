from utils.api import DiscordAPI

class GuildChannels:
    @staticmethod
    async def get_channels(guild_id):
        channels = await DiscordAPI.get(f"guilds/{guild_id}/channels")
        return channels
