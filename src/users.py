from utils.api import DiscordAPI

class Users:
    @staticmethod
    async def get_user(user_id=None):
        endpoint_suffix = str(user_id) or "@me"
        user = await DiscordAPI.get(f"users/{user_id}/{endpoint_suffix}")
        return user
    
    @staticmethod
    async def create_dm(user_id):
        await DiscordAPI.post("users/@me/channels", {
            "recipient_id": user_id
        })