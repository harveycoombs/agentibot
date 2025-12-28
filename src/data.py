import os
from datetime import datetime
#import redis
from supabase import create_client, Client
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

#def setup_guild_counter(count):
#    try:
#        rc = redis.Redis(host="localhost", port=6379, db=0)
#        rc.set("guild_count", count)

#        return rc
#    except Exception as e:
#        print(f"Unable to setup guild counter: {e}")
#        return None

def register_guild(guild_id, owner_id):
    try:
        response = supabase.table("vesper.guilds").insert({
            "guild_id": guild_id,
            "owner_id": owner_id,
            "registration_date": datetime.now().isoformat(),
            "interactions_this_month": 0,
            "interaction_start_date": datetime.now().isoformat()
        }).execute()

        if response.get("error"):
            print(f"Unable to register guild: {response['error']['message']}")
            return None
    except Exception as e:
        print(f"Unable to register guild: {e}")
        return None

def update_registered_guild_owner(guild_id, owner_id):
    try:
        response = supabase.table("vesper.guilds").update({ "owner_id": owner_id }).eq("guild_id", guild_id).execute()

        if response.get("error"):
            print(f"Unable to update registered guild owner: {response['error']['message']}")
            return None
    except Exception as e:
        print(f"Unable to update registered guild owner: {e}")
        return None

def get_guild_interaction_count(guild_id):
    try:
        response = supabase.table("vesper.guilds").select("interactions_this_month").eq("guild_id", guild_id).single().execute()

        if response.get("error"):
            print(f"Unable to get guild interaction count: {response['error']['message']}")
            return 0

        data = response.get("data")
        if not data or "interactions_this_month" not in data:
            return 0

        return data["interactions_this_month"]
    except Exception as e:
        print(f"Unable to get guild interaction count: {e}")
        return 0

def update_guild_interaction_count(guild_id):
    try:
        response = supabase.table("vesper.guilds").update({
            "interactions_this_month": supabase.rpc("increment_field", {
                "field_name": "interactions_this_month",
                "increment_by": 1
            })
        }).eq("guild_id", guild_id).execute()

        if response.get("error"):
            print(f"Unable to update guild interaction count: {response['error']['message']}")
            return False

        return bool(response.get("data"))
    except Exception as e:
        print(f"Unable to update guild interaction count: {e}")
        return False

def check_guild_interaction_limit_hit(guild_id):
    try:
        response = supabase.table("vesper.guilds").select("interactions_this_month, interaction_start_date").eq("guild_id", guild_id).single().execute()

        if response.get("error"):
            print(f"Unable to check guild interaction limit hit: {response['error']['message']}")
            return None

        data = response.get("data")

        if not data:
            return False

        interactions_this_month = data.get("interactions_this_month", 0)
        raw_interaction_start_date = data.get("interaction_start_date")

        if interactions_this_month is None or raw_interaction_start_date is None:
            return False

        interaction_start_date = datetime.fromisoformat(raw_interaction_start_date.rstrip("Z"))

        now = datetime.now()
        one_month_ago = now - timedelta(days=30)

        if (interactions_this_month >= 200 and interaction_start_date >= one_month_ago):
            return True

        return False
    except Exception as e:
        print(f"Unable to check guild interaction limit hit: {e}")
        return None

def guild_is_registered(guild_id):
    try:
        response = supabase.table("vesper.guilds").select("guild_id").eq("guild_id", guild_id).single().execute()

        if response.get("error"):
            if response["error"]["code"] == "PGRST116":
                return False

            print(f"Unable to check if guild is registered: {response['error']['message']}")
            return False

        data = response.get("data")
        return bool(data and data.get("guild_id") == guild_id)
    except Exception as e:
        print(f"Unable to check if guild is registered: {e}")
        return False

def insert_error_log(guild_id, author_id, prompt, error_message):
    try:
        response = supabase.table("vesper.errors").insert({
            "incident_date": datetime.now().isoformat(),
            "guild_id": guild_id,
            "author_id": author_id,
            "prompt": prompt,
            "error": error_message
        }).execute()

        if response.get("error"):
            print(f"Unable to insert error log: {response['error']['message']}")
            return False

        return bool(response.get("data"))
    except Exception as e:
        print(f"Unable to insert error log: {e}")
        return False

def get_model_choice(guild_id):
    try:
        guild_response = supabase.table("vesper.guilds").select("owner_id").eq("guild_id", guild_id).single().execute()

        if guild_response.get("error"):
            print(f"Unable to get guild owner_id: {guild_response['error']['message']}")
            return "gpt-5-nano"

        guild_data = guild_response.get("data")
        owner_id = guild_data.get("owner_id") if guild_data else None

        if not owner_id:
            return "gpt-5-nano"

        user_response = supabase.table("vesper.users").select("model").eq("user_id", owner_id).single().execute()

        if user_response.get("error"):
            print(f"Unable to get user model: {user_response['error']['message']}")
            return "gpt-5-nano"

        user_data = user_response.get("data")

        if not user_data or user_data.get("model") is None:
            return "gpt-5-nano"

        return user_data["model"]
    except Exception as e:
        print(f"Unable to get model choice: {e}")
        return "gpt-5-nano"