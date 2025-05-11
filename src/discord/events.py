import json

from utils.status import update_guild_counter
from discord.messages import Messages
from ai.agent import Agent

CONFIG = json.load(open("../config.json"))

class Events:
    @staticmethod
    async def handle(raw):
        event = json.loads(raw)

        event_type = event["t"]
        event_data = event["d"]

        match event_type:
            case "READY":
                guild_count = len(event_data["guilds"])
                update_guild_counter(guild_count)

                print(f"Discord Gateway: Ready in {guild_count} guilds")
                return
            case "MESSAGE_CREATE":
                author_id = event_data["author"]["id"]
                channel_id = event_data["channel_id"]

                if author_id == CONFIG["application_id"] or CONFIG["application_id"] not in [mention["id"] for mention in event_data["mentions"]]:
                    return

                try:
                    agent = Agent(context=event_data)
                    response = await agent.respond(event_data["content"].replace(f"<@!{CONFIG['application_id']}>", ""))

                    await Messages.create_message(channel_id, response)
                except Exception as e:
                    await Messages.create_message(channel_id, f":x: Something went wrong. Please try again later.")
                    print(e)
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
                            "label": "Website",
                            "style": 5,
                            "url": "https://vesper.gg"
                        }
                    ]
                }])
                return