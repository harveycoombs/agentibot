from discord.api import DiscordAPI

class Channels:
    @staticmethod
    async def get_channels(guild_id):
        channels = await DiscordAPI.get(f"guilds/{guild_id}/channels")
        return channels

    @staticmethod
    async def create_channel(guild_id, channel_name, channel_type=0):
        response = await DiscordAPI.post(f"guilds/{guild_id}/channels", {
            "name": channel_name,
            "type": channel_type
        })

        return response["id"]

    @staticmethod
    async def delete_channel(channel_id):
        await DiscordAPI.delete(f"channels/{channel_id}")