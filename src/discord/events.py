import os
import json
import yaml
import redis

from data import update_guild_interaction_count, check_guild_interaction_limit_hit, register_guild, guild_is_registered, insert_error_log, update_registered_guild_owner, get_settings
from discord.messages import Messages
from ai.agent import Agent
from exception import VesperException

CONFIG = yaml.safe_load(open(f"{os.getcwd().replace("\\", "/")}/config.yaml"))

rc = redis.Redis(host="localhost", port=6379, db=0)

class Events:
    @staticmethod
    async def handle(raw):
        event = json.loads(raw)

        event_type = event["t"]
        event_data = event["d"]

        match event_type:
            case "READY":
                rc.set("guild_count", len(event_data["guilds"]))
                print(f"Vesper is ready in {len(event_data['guilds'])} guilds.")
                return

            case "MESSAGE_CREATE":
                author_id = event_data["author"]["id"]
                channel_id = event_data["channel_id"]
                guild_id = event_data["guild_id"]

                settings = get_settings(guild_id)
                model = settings["model"] if settings is not None else "mistral"

                if author_id == CONFIG["application_id"] or CONFIG["application_id"] not in [mention["id"] for mention in event_data["mentions"]]:
                    return

                guild_id = event_data["guild_id"]

                if CONFIG["application_id"] != "1365463510934360135":
                    if check_guild_interaction_limit_hit(guild_id):
                        await Messages.create_message(channel_id, f":warning: You've reached your monthly interaction limit. [Click here](https://vesper.gg/pro) to learn more.")
                        return

                    update_guild_interaction_count(guild_id)

                try:
                    agent = Agent(context=event_data, model=model)
                    response = await agent.respond(event_data["content"].replace(f"<@!{CONFIG['application_id']}>", ""))

                    await Messages.create_message(channel_id, response["output"])
                except VesperException as ve:
                    await Messages.create_message(channel_id, f"{ve}")
                    return
                except Exception as e:
                    insert_error_log(guild_id, author_id, event_data["content"], str(e))
                    await Messages.create_message(channel_id, ":bangbang: Something went wrong. Please try again later.")
                    return
                
            case "GUILD_CREATE":
                guild_id = event_data["id"]
                owner_id = event_data["owner_id"]

                if not guild_is_registered(guild_id):
                    register_guild(guild_id, owner_id)

                    system_channel_id = event_data["system_channel_id"]

                    rc.incr("guild_count")                

                    await Messages.create_message(system_channel_id, None, [{
                        "title": ":wave: Thank you for inviting me to your server!",
                        "description": "Check out the [Documentation](https://harvey-coombs-1.gitbook.io/vesper) to get started.",
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
                else:
                    update_registered_guild_owner(guild_id, owner_id)

            case "GUILD_UPDATE":
                update_registered_guild_owner(event_data["guild_id"], event_data["owner_id"])
                return
            
            case "GUILD_DELETE":
                rc.decr("guild_count")
                return