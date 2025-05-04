import json

from utils.api import DiscordAPI

CONFIG = json.load(open("../config.json"))

class Messages:
    embed_color = CONFIG["embed_color"]

    @staticmethod
    async def get_messages(channel_id):
        messages = await DiscordAPI.get(f"channels/{channel_id}/messages")
        return messages
    
    async def get_message(channel_id, message_id):
        message = await DiscordAPI.get(f"channels/{channel_id}/messages/{message_id}")
        return message
    
    async def create_message(channel_id, content, embeds=None, components=None):
        await DiscordAPI.post(f"channels/{channel_id}/messages", {
            "content": content,
            "tts": False,
            "embeds": embeds or [],
            "components": components or []
        })

    async def update_message(channel_id, message_id, content=None, embeds=None):
        await DiscordAPI.patch(f"channels/{channel_id}/messages/{message_id}", {
            "content": content,
            "embeds": embeds or []
        })

    async def delete_message(channel_id, message_id):
        await DiscordAPI.delete(f"channels/{channel_id}/messages/{message_id}")

    @staticmethod
    async def add_reaction(channel_id, message_id, emoji):
        await DiscordAPI.post(f"channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me", payload=None)