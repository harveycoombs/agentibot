from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

from ai.toolchain import add_role, remove_role, change_nickname, create_text_channel, create_voice_channel, delete_channel, delete_message

class Agent:
    def __init__(self, context: dict):
        self.context = context

        self.tools = [
            Tool(
                name="add_role",
                func=None,
                description="Adds a role to a user. Input should be a string with the role's name.",
                coroutine=lambda x: add_role(x, self.context["guild_id"], self.context["author"]["id"])
            ),
            Tool(
                name="remove_role",
                func=None,
                description="Removes a role from a user. Input should be a string with the role's name.",
                coroutine=lambda x: remove_role(x, self.context["guild_id"], self.context["author"]["id"])
            ),
            Tool(
                name="change_nickname",
                func=None,
                description="Changes the nickname of a user. Input should be a string with the new nickname.",
                coroutine=lambda x: change_nickname(x, self.context["guild_id"], self.context["author"]["id"])
            ),
            Tool(
                name="create_text_channel",
                func=None,
                description="Creates a text channel. Input should be a string with the channel's name.",
                coroutine=lambda x: create_text_channel(x, self.context["guild_id"])
            ),
            Tool(
                name="create_voice_channel",
                func=None,
                description="Creates a voice channel. Input should be a string with the channel's name.",
                coroutine=lambda x: create_voice_channel(x, self.context["guild_id"])
            ),
            Tool(
                name="delete_channel",
                func=None,
                description="Deletes the current channel.",
                coroutine=lambda x: delete_channel(x, self.context["channel_id"])
            ),
            Tool(
                name="delete_message",
                func=None,
                description="Deletes a message. Input should be a string with the message's content.",
                coroutine=lambda x: delete_message(x)
            )
        ]

        self.agent = initialize_agent(
            tools=self.tools,
            llm=ChatOllama(model="gemma3:12b"),
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False
        )

    async def respond(self, prompt: str):
        return await self.agent.arun(prompt)