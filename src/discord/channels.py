from discord.api import DiscordAPI

class Channels:
    @staticmethod
    async def get_channels(guild_id):
        try:
            channels = await DiscordAPI.get(f"guilds/{guild_id}/channels")
            return channels
        except Exception:
            raise Exception(":bangbang: Unable to retrieve channels.")

    @staticmethod
    async def create_channel(guild_id, channel_name, channel_type=0):
        try:
            response = await DiscordAPI.post(f"guilds/{guild_id}/channels", {
                "name": channel_name,
                "type": channel_type
            })

            return response["id"]
        except Exception:
            raise Exception(":bangbang: Unable to create channel.")

    @staticmethod
    async def delete_channel(channel_id):
        try:
            await DiscordAPI.delete(f"channels/{channel_id}")
        except Exception:
            raise Exception(":bangbang: Unable to delete channel.")