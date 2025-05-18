import mysql.connector
import json

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