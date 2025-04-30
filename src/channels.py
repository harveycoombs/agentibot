from utils.api import DiscordAPI

class Channels:
    @staticmethod
    async def get_channels(guild_id):
        channels = await DiscordAPI.get(f"guilds/{guild_id}/channels")
        return channels

    @staticmethod
    async def create_channel(guild_id, channel_name):
        await DiscordAPI.post(f"guilds/{guild_id}/channels", {
            "name": channel_name
        })
