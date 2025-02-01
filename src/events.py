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

                    messages = await Messages.get_messages(channel_id)
                    response = await AI.generate_text_response(event_data["content"], messages)

                    await Messages.create_message(channel_id, response)
                return
            case "MESSAGE_UPDATE":
                #await Messages.create_message(system_channel_id, None, [{
                #    "author": {
                #        "name": message_author["username"],
                #        "icon_url": message_author["avatar_url"]
                #    },
                #    "title": ":pencil2: Message Edited",
                #    "description": f"`{message['content']}`",
                #    "color": Messages.embed_color
                #}])
                return
            case "MESSAGE_DELETE":
                #await Messages.create_message(system_channel_id, None, [{
                #    "author": {
                #        "name": message_author["username"],
                #        "icon_url": message_author["avatar_url"]
                #    },
                #    "title": ":wastebasket: Message Deleted",
                #    "description": f"`{message['content']}`",
                #    "color": Messages.embed_color
                #}])
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