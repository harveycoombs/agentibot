import os
import yaml
import asyncio

from discord.api import DiscordAPI
from exception import VesperException

CONFIG = yaml.safe_load(open(f"{os.getcwd().replace("\\", "/")}/config.yaml"))

class Messages:
    embed_color = CONFIG["embed_color"]

    @staticmethod
    async def get_messages(channel_id):
        try:
            messages = await DiscordAPI.get(f"channels/{channel_id}/messages")
            return messages
        except Exception:
            raise VesperException(":bangbang: Unable to retrieve messages.")

    @staticmethod    
    async def create_message(channel_id, content, embeds=None, components=None):
        try:
            await DiscordAPI.post(f"channels/{channel_id}/messages", {
                "content": content,
                "tts": False,
                "embeds": embeds or [],
                "components": components or []
            })
        except Exception:
            raise VesperException(":bangbang: Unable to create message.")

    @staticmethod
    async def update_message(channel_id, message_id, content=None, embeds=None):
        try:
            await DiscordAPI.patch(f"channels/{channel_id}/messages/{message_id}", {
                "content": content,
                "embeds": embeds or []
            })
        except Exception:
            raise VesperException(":bangbang: Unable to update message.")

    @staticmethod
    async def delete_message(channel_id, message_id):
        try:
            await DiscordAPI.delete(f"channels/{channel_id}/messages/{message_id}")
        except Exception:
            raise VesperException(":bangbang: Unable to delete message.")

    @staticmethod
    async def bulk_delete_messages(channel_id, amount):
        try:
            messages = await DiscordAPI.get(f"channels/{channel_id}/messages")

            for x in range(int(amount) + 1):
                await DiscordAPI.delete(f"channels/{channel_id}/messages/{messages[x]['id']}")
                await asyncio.sleep(0.75)
        except Exception:
            raise VesperException(":bangbang: Unable to bulk delete messages.")