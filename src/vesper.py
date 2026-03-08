# Vesper ~ vesperbot.ai ~ Written by Harvey Coombs ~ 2020-2024
import asyncio
from discord.gateway import Gateway
from dotenv import load_dotenv

load_dotenv()

async def main():
    while True:
        try:
            await Gateway.connect()
        except Exception as ex:
            print(ex)

        await asyncio.sleep(4)

asyncio.run(main())