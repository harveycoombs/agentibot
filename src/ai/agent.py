from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

from ai.toolchain import get_bot_creator, add_role, remove_role, create_role, change_nickname, create_text_channel, create_voice_channel, delete_channel, delete_message, ban_member, unban_member, kick_member, bulk_delete_messages

class Agent:
    def __init__(self, context: dict):
        self.context = context

        self.tools = [
            Tool(
                name="get_bot_creator",
                func=lambda _: get_bot_creator(),
                description="Gets the creator of the bot, which is you."
            ),
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
                name="create_role",
                func=None,
                coroutine=lambda x: create_role(x.split(" ")[0], x.split(" ")[1], self.context["guild_id"], self.context["author"]["id"]),
                description="Creates a role. Input should be a string with the role's name and a string with the role's hex color."
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
                coroutine=lambda x: create_text_channel(x, self.context["guild_id"], self.context["author"]["id"]),
                description="Creates a text channel. Input should be a string with the channel's name."
            ),
            Tool(
                name="create_voice_channel",
                func=None,
                coroutine=lambda x: create_voice_channel(x, self.context["guild_id"], self.context["author"]["id"]),
                description="Creates a voice channel. Input should be a string with the channel's name."
            ),
            Tool(
                name="delete_channel",
                func=None,
                coroutine=lambda x: delete_channel(x, self.context["guild_id"], self.context["author"]["id"]),
                description="Deletes the current channel."
            ),
            Tool(
                name="delete_message",
                func=None,
                coroutine=lambda _: delete_message(self.context["channel_id"], self.context["message_reference"], self.context["guild_id"], self.context["author"]["id"]),
                description="Deletes a message. Input should be a string with the message's content."
            ),
            Tool(
                name="bulk_delete_messages",
                func=None,
                coroutine=lambda x: bulk_delete_messages(x, self.context["channel_id"], self.context["guild_id"], self.context["author"]["id"]),
                description="Bulk deletes messages in the current channel. Input should be a number with the amount of messages to delete."
            ),
            Tool(
                name="ban_member",
                func=None,
                coroutine=lambda x: ban_member(x, self.context["guild_id"], self.context["mentions"][1]["id"],),
                description="Bans a member. Input should be a string with the member's ID."
            ),
            Tool(
                name="unban_member",
                func=None,
                coroutine=lambda x: unban_member(x, self.context["guild_id"], self.context["mentions"][1]["id"], self.context["author"]["id"]),
                description="Unbans a member. Input should be a string with the member's ID."
            ),
            Tool(
                name="kick_member",
                func=None,
                coroutine=lambda _: kick_member(self.context["mentions"][1]["id"], self.context["guild_id"], self.context["author"]["id"]),
                description="Kicks a member. Input should be a string with the member's ID."
            )
        ]

        self.agent = initialize_agent(
            tools=self.tools,
            llm=ChatOllama(model="qwen3:14b"),
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False,
            handle_parsing_errors=True
        )

    async def respond(self, prompt: str):
        return await self.agent.ainvoke(prompt)