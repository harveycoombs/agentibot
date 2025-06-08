import mysql.connector
import json
from datetime import datetime

CONFIG = json.load(open("../config.json"))

def update_guild_counter(count):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            database=CONFIG["database"]["schema"]
        )

        if not connection:
            print(f"Failed to connect to database.")

        cursor = connection.cursor(dictionary=True)
        cursor.execute("UPDATE bot_stats SET server_count = %s", (count,))
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Unable to update guild counter: {e}")
        return None
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

def get_guild_count():
    connection = None

    try:
        connection = mysql.connector.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            database=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT server_count FROM bot_stats")
        result = cursor.fetchone()

        return result["server_count"]
    except mysql.connector.Error as e:
        print(f"Unable to get guild count: {e}")
        return None
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

def register_guild(guild_id):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            database=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("INSERT INTO registered_guilds (guild_id, registration_date, interactions_this_month, interaction_start_date) VALUES (%s, %s, %s, %s)", (guild_id, datetime.now(), 0, datetime.now()))
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Unable to register guild: {e}")
        return None
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

def get_guild_interaction_count(guild_id):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            database=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT interactions_this_month FROM registered_guilds WHERE guild_id = %s", (guild_id,))
        result = cursor.fetchone()

        if result is None:
            return 0

        return result["interactions_this_month"]
    except mysql.connector.Error as e:
        print(f"Unable to get guild interaction count: {e}")
        return 0
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

def update_guild_interaction_count(guild_id):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            database=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("UPDATE registered_guilds SET interactions_this_month = interactions_this_month + 1 WHERE guild_id = %s", (guild_id,))
        connection.commit()

        return cursor.rowcount > 0
    except mysql.connector.Error as e:
        print(f"Unable to update guild interaction count: {e}")
        return False
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

def check_guild_interaction_limit_hit(guild_id):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            database=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS n FROM registered_guilds WHERE interactions_this_month >= 200 AND interaction_start_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH) AND guild_id = %s", (guild_id,))
        result = cursor.fetchone()

        return result["n"] > 0
    except mysql.connector.Error as e:
        print(f"Unable to check guild interaction limit hit: {e}")
        return None
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

def guild_is_registered(guild_id):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=CONFIG["database"]["host"],
            user=CONFIG["database"]["user"],
            password=CONFIG["database"]["password"],
            database=CONFIG["database"]["schema"]
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS n FROM registered_guilds WHERE guild_id = %s", (guild_id,))
        result = cursor.fetchone()

        return result["n"] > 0
    except mysql.connector.Error as e:
        print(f"Unable to check if guild is registered: {e}")
        return False
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()