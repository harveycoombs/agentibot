import json

from messages import Messages
from utils.ai import AI

CONFIG = json.load(open("../config.json"))

class Events:
    @staticmethod
    async def handle(raw):
        event = json.loads(raw)

        event_type = event["t"]
        event_data = event["d"]

        match event_type:
            case "READY":
                print(f"Discord Gateway: Ready")
                return
            case "MESSAGE_CREATE":
                message_author_id = event_data["author"]["id"]

                if message_author_id != CONFIG["application_id"]:
                    channel_id = event_data["channel_id"]

                    response = await AI.respond_to_command(event_data["content"])

                    if response.startswith("ADD_ROLE"):
                        role_name = response.split("ADD_ROLE ")[1]
                        await Messages.create_message(channel_id, f"Added the {role_name} role to you.")
                    elif response.startswith("REMOVE_ROLE"):
                        role_name = response.split("REMOVE_ROLE ")[1]
                        await Messages.create_message(channel_id, f"Removed the {role_name} role from you.")
                    else:
                        await Messages.create_message(channel_id, response)
                return
            case "GUILD_CREATE":
                system_channel_id = event_data["system_channel_id"]


                await Messages.create_message(system_channel_id, None, [{
                    "title": ":wave: Thank you for inviting me to your server!",
                    "description": "Use the `/help` command to get started.",
                    "color": Messages.embed_color
                }], [{
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "View on GitHub",
                            "style": 5,
                            "url": "https://github.com/harveycoombs/discord-bot"
                        }
                    ]
                }])
                return