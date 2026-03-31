from datetime import datetime

class Utils:
    @staticmethod
    def snowflake_to_datetime(snowflake: int):
        timestamp = (snowflake >> 22) + 1420070400000
        date = datetime.fromtimestamp(timestamp / 1000)

        return date.strftime("%d %B %Y")