import os
import psycopg
from datetime import datetime
import yaml

CONFIG = yaml.safe_load(open(f"{os.getcwd().replace("\\", "/")}/config.yaml"))

def register_guild(guild_id, owner_id):
    connection = None

    try:
        connection = psycopg.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            dbname=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(row_factory=psycopg.rows.dict_row)

        cursor.execute("INSERT INTO vesper.registered_guilds (guild_id, owner_id, registration_date, interactions_this_month, interaction_start_date) VALUES (%s, %s, %s, %s, %s)", (guild_id, owner_id, datetime.now(), 0, datetime.now()))
        connection.commit()
    except psycopg.Error as e:
        print(f"Unable to register guild: {e}")
        return None
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def update_registered_guild_owner(guild_id, owner_id):
    connection = None

    try:
        connection = psycopg.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            dbname=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(row_factory=psycopg.rows.dict_row)

        cursor.execute("UPDATE vesper.registered_guilds SET owner_id = %s WHERE guild_id = %s", (owner_id, guild_id))
        connection.commit()
    except psycopg.Error as e:
        print(f"Unable to update registered guild owner: {e}")
        return None
    finally:
        if connection is not None:
            cursor.close()
            connection.close()    

def get_guild_interaction_count(guild_id):
    connection = None

    try:
        connection = psycopg.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            dbname=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(row_factory=psycopg.rows.dict_row)

        cursor.execute("SELECT interactions_this_month FROM vesper.registered_guilds WHERE guild_id = %s", (guild_id,))
        result = cursor.fetchone()

        if result is None:
            return 0

        return result["interactions_this_month"]
    except psycopg.Error as e:
        print(f"Unable to get guild interaction count: {e}")
        return 0
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def update_guild_interaction_count(guild_id):
    connection = None

    try:
        connection = psycopg.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            dbname=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(row_factory=psycopg.rows.dict_row)

        cursor.execute("UPDATE vesper.registered_guilds SET interactions_this_month = interactions_this_month + 1 WHERE guild_id = %s", (guild_id,))
        connection.commit()

        return cursor.rowcount > 0
    except psycopg.Error as e:
        print(f"Unable to update guild interaction count: {e}")
        return False
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def check_guild_interaction_limit_hit(guild_id):
    connection = None

    try:
        connection = psycopg.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            dbname=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(row_factory=psycopg.rows.dict_row)

        cursor.execute("SELECT COUNT(*) AS n FROM vesper.registered_guilds WHERE interactions_this_month >= 200 AND interaction_start_date >= NOW() - INTERVAL '1 month' AND guild_id = %s", (guild_id,))
        result = cursor.fetchone()

        return result["n"] > 0
    except psycopg.Error as e:
        print(f"Unable to check guild interaction limit hit: {e}")
        return None
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def guild_is_registered(guild_id):
    connection = None

    try:
        connection = psycopg.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            dbname=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(row_factory=psycopg.rows.dict_row)

        cursor.execute("SELECT COUNT(*) AS n FROM vesper.registered_guilds WHERE guild_id = %s", (guild_id,))
        result = cursor.fetchone()

        return result["n"] > 0
    except psycopg.Error as e:
        print(f"Unable to check if guild is registered: {e}")
        return False
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def insert_error_log(guild_id, author_id, prompt, error_message):
    connection = None

    try:
        connection = psycopg.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            dbname=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(row_factory=psycopg.rows.dict_row)

        cursor.execute("INSERT INTO vesper.errors (error_id, incident_date, guild_id, author_id, prompt, error) VALUES(gen_random_uuid(), NOW(), %s, %s, %s, %s)", (guild_id, author_id, prompt, error_message))
        connection.commit()

        return cursor.rowcount > 0
    except psycopg.Error as e:
        print(f"Unable to update guild interaction count: {e}")
        return False
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def get_settings(guild_id):
    connection = None

    try:
        connection = psycopg.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            dbname=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(row_factory=psycopg.rows.dict_row)

        cursor.execute("SELECT * FROM vesper.user_settings WHERE user_id = (SELECT owner_id FROM vesper.registered_guilds WHERE guild_id = %s)", (guild_id,))
        result = cursor.fetchone()

        return result
    except psycopg.Error as e:
        print(f"Unable to get user settings: {e}")
        return None
    finally:
        if connection is not None:
            cursor.close()
            connection.close()