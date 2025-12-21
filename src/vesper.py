# Vesper ~ vesperbot.ai ~ Written by Harvey Coombs ~ 2020–2024
import asyncio
import signal
import logging
from discord.gateway import Gateway

logging.basicConfig(level=logging.INFO)

shutdown_event = asyncio.Event()

def _shutdown():
    logging.info("Received shutdown signal")
    shutdown_event.set()

signal.signal(signal.SIGTERM, lambda *_: _shutdown())
signal.signal(signal.SIGINT, lambda *_: _shutdown())

async def main():
    delay = 2
    max_delay = 60

    while not shutdown_event.is_set():
        try:
            logging.info("Connecting to Discord gateway")
            await Gateway.connect()
            logging.info("Gateway exited gracefully")

            delay = 2
        except Exception as ex:
            logging.exception("Gateway encountered an exception")

        if shutdown_event.is_set():
            break

        logging.info(f"Reconnecting to gateway in {delay} seconds")
        await asyncio.sleep(delay)
        delay = min(delay * 2, max_delay)

if __name__ == "__main__":
    asyncio.run(main())