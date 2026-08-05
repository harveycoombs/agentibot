import os
import json
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv
from stripe import StripeClient

load_dotenv()

stripe_client = StripeClient(os.getenv("STRIPE_SECRET_KEY"))
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def register_guild(guild_id, owner_id):
    try:
        supabase.table("guilds").insert({
            "guild_id": guild_id,
            "owner_id": owner_id,
            "registration_date": datetime.now().isoformat(),
            "interactions_this_month": 0,
            "interaction_start_date": datetime.now().isoformat()
        }).execute()
    except Exception as e:
        print(f"Unable to register guild: {e}")

def get_registered_guild_owner(guild_id):
    try:
        response = supabase.table("guilds").select("owner_id").eq("guild_id", guild_id).maybe_single().execute()
        return response.data["owner_id"] if response.data else None
    except Exception as e:
        print(f"Unable to get registered guild owner: {e}")
        return None

def update_registered_guild_owner(guild_id, owner_id):
    try:
        supabase.table("guilds").update({ "owner_id": owner_id }).eq("guild_id", guild_id).execute()
    except Exception as e:
        print(f"Unable to update registered guild owner: {e}")

def get_guild_interaction_count(guild_id):
    try:
        response = supabase.table("guilds").select("interactions_this_month").eq("guild_id", guild_id).maybe_single().execute()
        return response.data["interactions_this_month"] if response.data else 0
    except Exception as e:
        print(f"Unable to get guild interaction count: {e}")
        return 0

def set_guild_interaction_count(guild_id, count):
    try:
        supabase.table("guilds").update({ "interactions_this_month": count }).eq("guild_id", guild_id).execute()
    except Exception as e:
        print(f"Unable to set guild interaction count: {e}")

def guild_is_registered(guild_id):
    try:
        response = supabase.table("guilds").select("guild_id").eq("guild_id", guild_id).maybe_single().execute()
        return bool(response.data and response.data["guild_id"] == guild_id)
    except Exception as e:
        print(f"Unable to check if guild is registered: {e}")
        return False

def insert_error_log(guild_id, author_id, prompt, error_message):
    print(f"ERR: {error_message}")

    try:
        response = supabase.table("errors").insert({
            "incident_date": datetime.now().isoformat(),
            "guild_id": guild_id,
            "author_id": author_id,
            "prompt": prompt,
            "error": error_message
        }).execute()

        return bool(response.data)
    except Exception as e:
        print(f"Unable to insert error log: {e}")

def get_model_choice(guild_id):
    try:
        guild_response = supabase.table("guilds").select("owner_id").eq("guild_id", guild_id).maybe_single().execute()
        guild_data = guild_response.data

        if not guild_data:
            print("Unable to get guild owner_id")
            return "gpt-5.4-nano"

        owner_id = guild_data["owner_id"] if guild_data else None

        if not owner_id:
            return "gpt-5.4-nano"

        user_response = supabase.table("users").select("model").eq("user_id", owner_id).maybe_single().execute()
        user_data = user_response.data

        if not user_data or user_data["model"] is None:
            print("Unable to get user model")
            return "gpt-5.4-nano"

        return user_data["model"]
    except Exception as e:
        print(f"Unable to get model choice: {e}")
        return "gpt-5.4-nano"
