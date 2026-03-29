import os
import json

from data import get_guild_interaction_count, set_guild_interaction_count, check_guild_interaction_limit_hit, register_guild, guild_is_registered, insert_error_log, update_registered_guild_owner, get_model_choice
from kv import get_kv, set_kv
from discord.messages import Messages
from ai.agent import Agent
from exception import VesperException
from discord.guilds import Guilds
from discord.utils import Utils

class Events:
    @staticmethod
    async def handle(raw):
        event = json.loads(raw)

        event_type = event["t"]
        event_data = event["d"]

        match event_type:
            case "READY":
                set_kv("guild_count", len(event_data["guilds"]))
                print(f"Vesper is ready in {len(event_data['guilds'])} guilds.")
                return

            case "MESSAGE_CREATE":
                author_id = event_data["author"]["id"]
                channel_id = event_data["channel_id"]
                guild_id = event_data["guild_id"]

                model = get_model_choice(guild_id)

                if author_id == os.getenv("APPLICATION_ID") or os.getenv("APPLICATION_ID") not in [mention["id"] for mention in event_data["mentions"]]:
                    return

                guild_id = event_data["guild_id"]

                if check_guild_interaction_limit_hit(guild_id):
                    await Messages.create_message(channel_id, ":warning: You've reached your monthly interaction limit. Visit the [Pricing](https://vesperbot.ai/pricing) page to learn more about increasing your limit.")
                    return

                interaction_count = get_guild_interaction_count(guild_id)
                set_guild_interaction_count(guild_id, interaction_count + 1)

                try:
                    agent = Agent(context=event_data, model=model)
                    response = await agent.respond(event_data["content"].replace(f"<@!{os.getenv('APPLICATION_ID')}>", "").strip())

                    if len(response) > 2000:
                        for x in range(0, len(response), 2000):
                            await Messages.create_message(channel_id, response[x:x+2000])
                    else:
                        await Messages.create_message(channel_id, response)
                except VesperException as ve:
                    await Messages.create_message(channel_id, f"{ve}")
                    return
                except Exception as e:
                    insert_error_log(guild_id, author_id, event_data["content"], str(e))
                    await Messages.create_message(channel_id, ":bangbang: Something went wrong. If this issue persists, [Contact Support](https://www.vesperbot.ai/contact) for further assistance.")
                    return
                
            case "GUILD_CREATE":
                guild_id = event_data["id"]
                owner_id = event_data["owner_id"]

                if not guild_is_registered(guild_id):
                    register_guild(guild_id, owner_id)

                    system_channel_id = event_data["system_channel_id"]         

                    set_kv("guild_count", get_kv("guild_count") + 1)

                    await Messages.create_message(system_channel_id, None, [{
                        "title": ":wave: Thank you for inviting me to your server!",
                        "description": "Check out the [About page](https://www.vesperbot.ai/about) to get started.",
                        "color": Messages.embed_color
                    }], [{
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "label": "Website",
                                "style": 5,
                                "url": "https://www.vesperbot.ai"
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
                set_kv("guild_count", get_kv("guild_count") - 1)
                return

            case "GUILD_MEMBER_REMOVE":
                member = event_data["user"]

                guild = await Guilds.get_guild(event_data["guild_id"])
                system_channel_id = guild["system_channel_id"]

                avatar_url = f"https://cdn.discordapp.com/avatars/{member['id']}/{member['avatar']}.webp"
                creation_date = Utils.snowflake_to_datetime(int(member["id"]))

                await Messages.create_message(system_channel_id, None, [{
                    "title": f":outbox_tray: {member['global_name']} left the server",
                    "description": f"Joined Discord on `{creation_date}`",
                    "author": {
                        "name": member["username"] or "Unknown User",
                        "icon_url": avatar_url
                    },
                    "thumbnail": {
                        "url": avatar_url
                    },
                    "footer": {
                        "text": f"{guild['name']} now has {guild['approximate_member_count'] or "?"} members",
                        "icon_url": f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}.webp"
                    },
                    "color": Messages.embed_color
                }])
                return

            case "GUILD_MEMBER_ADD":
                member = event_data["user"]

                guild = await Guilds.get_guild(event_data["guild_id"])
                system_channel_id = guild["system_channel_id"]

                avatar_url = f"https://cdn.discordapp.com/avatars/{member['id']}/{member['avatar']}.webp"
                creation_date = Utils.snowflake_to_datetime(int(member["id"]))

                await Messages.create_message(system_channel_id, None, [{
                    "title": f":inbox_tray: {member['global_name']} joined the server",
                    "description": f"Joined Discord on `{creation_date}`",
                    "author": {
                        "name": member["username"] or "Unknown User",
                        "icon_url": avatar_url
                    },
                    "thumbnail": {
                        "url": avatar_url
                    },
                    "footer": {
                        "text": f"{guild['name']} now has {guild['approximate_member_count'] or "?"} members",
                        "icon_url": f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}.webp"
                    },
                    "color": Messages.embed_color
                }])
                return