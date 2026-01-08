import json
from langchain.agents import create_agent

from ai.toolchain import get_bot_creator, get_server_info, add_role, remove_role, create_role, change_nickname, create_text_channel, create_voice_channel, delete_channel, delete_message, ban_member, unban_member, kick_member, bulk_delete_messages, rename_channel, get_server_interaction_count, generate_image_from_prompt, create_server_invite, delete_server_invite, update_server

class Agent:
    def __init__(self, context: dict, model: str):
        self.context = context
        self.model = model

        self.agent = create_agent(
            model=self.model,
            tools=[get_bot_creator, get_server_info, add_role, remove_role, create_role, change_nickname, create_text_channel, create_voice_channel, delete_channel, delete_message, ban_member, unban_member, kick_member, bulk_delete_messages, rename_channel, get_server_interaction_count, generate_image_from_prompt, create_server_invite, delete_server_invite, update_server],
            system_prompt=f"You are Vesper, a helpful assistant that decides which tool is most appropriate to use based on the user's prompt, using both the user's prompt and the following data as parameters for each tool: {json.dumps(self.context)}"
        )

    async def respond(self, prompt: str):
        response = await self.agent.ainvoke({ "messages": [{ "role": "user", "content": prompt }]})
        return response["messages"][-1].content