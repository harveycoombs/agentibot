from utils.api import DiscordAPI

class Reactions:
    @staticmethod
    async def create_reaction(channel_id, message_id, emoji):
        await DiscordAPI.put(f"channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me")

    @staticmethod
    async def delete_reaction(channel_id, message_id, emoji, user_id=None):
        endpoint_suffix = str(user_id) or "@me"
        await DiscordAPI.delete(f"channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{endpoint_suffix}")