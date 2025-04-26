import json

from messages import Messages
from roles import Roles
from utils.ai import AI
from members import Members

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
                author_id = event_data["author"]["id"]
                guild_id = event_data["guild_id"]
                channel_id = event_data["channel_id"]

                if author_id == CONFIG["application_id"] or CONFIG["application_id"] not in [mention["id"] for mention in event_data["mentions"]]:
                    return

                try:
                    response = await AI.respond_to_command(event_data["content"].replace(f"<@!{CONFIG['application_id']}>", ""))

                    if "ADD_ROLE" in response:
                        role_name = response.split("ADD_ROLE ")[1].strip()
                        roles = await Roles.get_roles(guild_id)
                        role = next((role for role in roles if role["name"].lower() == role_name.lower()), None)

                        if role is None:
                            await Messages.create_message(channel_id, ":warning: Sorry, I couldn't find that role.")
                            return
                        
                        await Roles.add_role_to_user(guild_id, author_id, role["id"])
                        await Messages.create_message(channel_id, ":white_check_mark: I have added that role to you.")
                    elif "REMOVE_ROLE" in response:
                        role_name = response.split("REMOVE_ROLE ")[1].strip()
                        roles = await Roles.get_roles(guild_id)
                        role = next((role for role in roles if role["name"].lower() == role_name.lower()), None)

                        if role is None:
                            await Messages.create_message(channel_id, f":warning: Sorry, I couldn't find the '{role_name}' role.")
                            return
                        
                        await Roles.remove_role_from_user(guild_id, author_id, role["id"])
                        await Messages.create_message(channel_id, f":white_check_mark: I have removed the '{role_name}' role from you.")
                    elif "CHANGE_NICKNAME" in response:
                        nickname = response.split("CHANGE_NICKNAME ")[1].strip()
                        
                        await Members.update_member(guild_id, author_id, nickname)
                        await Messages.create_message(channel_id, f":white_check_mark: I have changed your nickname to '{nickname}'.")
                    else:
                        await Messages.create_message(channel_id, response)
                    return
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