import aiohttp
import json

CONFIG = json.load(open("../config.json"))

class DiscordAPI:
    BASE_URL = "https://discord.com/api/"
    @staticmethod
    async def get(endpoint, additional_headers=None):
        headers = dict({
            "Authorization": f"Bot {CONFIG['token']}",
            "Content-Type": "application/json"
        })
        
        if additional_headers is not None:
            headers.update(additional_headers)        

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{DiscordAPI.BASE_URL}{endpoint}", headers=headers) as response:
                try:
                    return await response.json()
                except:
                    return await response.text()


    @staticmethod
    async def post(endpoint, payload, additional_headers=None):
        headers = dict({
            "Authorization": f"Bot {CONFIG['token']}",
            "Content-Type": "application/json"
        })

        if additional_headers is not None:
            headers.update(additional_headers)
        
        async with aiohttp.ClientSession() as session:
            if payload is not None: 
                async with session.post(f"{DiscordAPI.BASE_URL}{endpoint}", json=payload, headers=headers) as response:
                    try:
                        return await response.json()

                    except:
                        return await response.text()
            else:
                async with session.post(f"{DiscordAPI.BASE_URL}{endpoint}", headers=headers) as response:
                    try:
                        return await response.json()
                    except:
                        return await response.text()



    @staticmethod
    async def patch(endpoint, payload, additional_headers=None):
        headers = dict({
            "Authorization": f"Bot {CONFIG['token']}",
            "Content-Type": "application/json"
        })

        if additional_headers is not None:
            headers.update(additional_headers)

        async with aiohttp.ClientSession() as session:
            async with session.patch(f"{DiscordAPI.BASE_URL}{endpoint}", json=payload, headers=headers) as response:
                try:
                    return await response.json()
                except:
                    return await response.text()


    @staticmethod
    async def put(endpoint, payload, additional_headers=None):
        headers = dict({
            "Authorization": f"Bot {CONFIG['token']}",
            "Content-Type": "application/json"
        })

        if additional_headers is not None:
            headers.update(additional_headers)

        async with aiohttp.ClientSession() as session:
            if payload is not None:
                async with session.put(f"{DiscordAPI.BASE_URL}{endpoint}", json=payload, headers=headers) as response:
                    try:
                        return await response.json()
                    except:
                        return await response.text()
            else:
                async with session.put(f"{DiscordAPI.BASE_URL}{endpoint}", headers=headers) as response:
                    try:
                        return await response.json()
                    except:
                        return await response.text()


    @staticmethod
    async def delete(endpoint, payload=None, additional_headers=None):
        headers = dict({
            "Authorization": f"Bot {CONFIG['token']}",
            "Content-Type": "application/json"
        })

        if additional_headers is not None:
            headers.update(additional_headers)     

        async with aiohttp.ClientSession() as session:
            if payload is not None:
                async with session.delete(f"{DiscordAPI.BASE_URL}{endpoint}", json=payload, headers=headers) as response:
                    try:
                        return await response.json()
                    except:
                        return await response.text()
            else:
                async with session.delete(f"{DiscordAPI.BASE_URL}{endpoint}", headers=headers) as response:
                    try:
                        return await response.json()
                    except:
                        return await response.text()
