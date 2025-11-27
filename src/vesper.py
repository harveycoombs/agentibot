# Vesper vesperbot.ai ~ Written by Harvey Coombs ~ 2020-2024
import asyncio
from discord.gateway import Gateway

async def main():
    while True:
        try:
            await Gateway.connect()
        except Exception as ex:
            print(f"Discord gateway raised an exception: {ex.message}")

        await asyncio.sleep(4)

asyncio.run(main())