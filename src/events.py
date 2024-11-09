import json

from messages import Messages
from models.text import TextModels

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
                    message_content = event_data["content"].replace(f"<@{CONFIG['application_id']}>", "").strip()

                    response = TextModels.generate_response(message_content)

                    await Messages.create_message(channel_id, f"<@{message_author_id}> {response}")
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