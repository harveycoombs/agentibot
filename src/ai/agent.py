from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

from ai.toolchain import add_role, remove_role, change_nickname, create_text_channel, create_voice_channel, delete_channel, delete_message, ban_member, unban_member, kick_member

class Agent:
    def __init__(self, context: dict):
        self.context = context

        self.tools = [
            Tool(
                name="add_role",
                func=None,
                coroutine=lambda x: add_role(x, self.context["guild_id"], self.context["author"]["id"]),
                description="Adds a role to a user. Input should be a string with the role's name."
            ),
            Tool(
                name="remove_role",
                func=None,
                coroutine=lambda x: remove_role(x, self.context["guild_id"], self.context["author"]["id"]),
                description="Removes a role from a user. Input should be a string with the role's name."
            ),
            Tool(
                name="change_nickname",
                func=None,
                coroutine=lambda x: change_nickname(x, self.context["guild_id"], self.context["author"]["id"]),
                description="Changes the nickname of a user. Input should be a string with the new nickname."
            ),
            Tool(
                name="create_text_channel",
                func=None,
                coroutine=lambda x: create_text_channel(x, self.context["guild_id"]),
                description="Creates a text channel. Input should be a string with the channel's name."
            ),
            Tool(
                name="create_voice_channel",
                func=None,
                coroutine=lambda x: create_voice_channel(x, self.context["guild_id"]),
                description="Creates a voice channel. Input should be a string with the channel's name."
            ),
            Tool(
                name="delete_channel",
                func=None,
                coroutine=lambda x: delete_channel(x, self.context["channel_id"]),
                description="Deletes the current channel."
            ),
            Tool(
                name="delete_message",
                func=None,
                coroutine=lambda x: delete_message(x),
                description="Deletes a message. Input should be a string with the message's content."
            ),
            Tool(
                name="ban_member",
                func=None,
                coroutine=lambda x: ban_member(x, self.context["guild_id"], self.context["mentions"][0]["id"]),
                description="Bans a member. Input should be a string with the member's ID."
            ),
            Tool(
                name="unban_member",
                func=None,
                coroutine=lambda x: unban_member(x, self.context["guild_id"], self.context["mentions"][0]["id"]),
                description="Unbans a member. Input should be a string with the member's ID."
            ),
            Tool(
                name="kick_member",
                func=None,
                coroutine=lambda x: kick_member(x, self.context["guild_id"], self.context["mentions"][0]["id"]),
                description="Kicks a member. Input should be a string with the member's ID."
            )
        ]

        self.agent = initialize_agent(
            tools=self.tools,
            llm=ChatOllama(model="gemma3:12b"),
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False
        )

    async def respond(self, prompt: str):
        return await self.agent.ainvoke(prompt)