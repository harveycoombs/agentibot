import json

from utils.api import DiscordAPI

CONFIG = json.load(open("../config.json"))

class Commands:
    @staticmethod
    async def register_command(name, description, options=[]):
        await DiscordAPI.post(f"applications/{CONFIG['application_id']}/commands", {
            "name": name,
            "type": 1,
            "description": description,
            "options": options or []
        })