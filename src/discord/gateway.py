import websockets
import asyncio
import json

from utils.api import DiscordAPI
from events import Events

CONFIG = json.load(open("../config.json"))

class Gateway:
    heartbeat = { "d": None, "op": 1 }

    identity = {
        "d": {
            "token": CONFIG["token"],
            "intents": 513,
            "properties": { "$os": "linux" }
        },
        "op": 2
    }

    presence = {
        "d": {
            "status": "online",
            'activities': [
                {
                    "name": "/help",
                    "type": 2
                }
            ],
            "since": None,
            "afk": False
        },
        "op": 3
    }

    @staticmethod
    async def get_gateway_url():
        gateway = await DiscordAPI.get("gateway/bot")
        return gateway["url"]
    
    @staticmethod
    async def keep_alive(socket, interval):
        while True:
            try:
                await asyncio.sleep(interval / 1000)
                await socket.send(json.dumps(Gateway.heartbeat))
            except Exception as ex:
                print(f"Discord gateway raised an exception: {ex}")

    
    @staticmethod
    async def connect():
        url = await Gateway.get_gateway_url()

        async with websockets.connect(url) as socket:
            response = await socket.recv()
            response_json = json.loads(response)
            heartbeat_interval = response_json["d"]["heartbeat_interval"]

            asyncio.create_task(Gateway.keep_alive(socket, heartbeat_interval))

            await socket.send(json.dumps(Gateway.identity))

            await socket.send(json.dumps(Gateway.presence))

            async for message in socket:
                await Events.handle(message)