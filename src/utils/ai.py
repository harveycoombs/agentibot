import ollama

class AI:
    @staticmethod
    def format_message(message):
        return {
            "role": "assistant" if message["author"]["bot"] else "user",
            "content": message["content"]
        }

    @staticmethod
    async def generate_text_response(messages, model="deepseek-v2:lite"):
        context = map(AI.format_message, messages)

        response = ollama.chat(model=model, messages=context)
        return response["message"]["content"]
    
    
    @staticmethod
    async def respond_to_command(prompt, messages=[]):
        message_history = map(AI.format_message, messages)

        all_messages = list(message_history) + [{
            "role": "user",
            "content": f"""
                You are Vesper, an intelligent AI Discord bot created by Harvey Coombs. Your purpose is to assist users with various Discord-related tasks.

                INSTRUCTIONS:
                Analyze the user's prompt below and determine their intent. If they are requesting one of the following actions, respond ONLY with the exact command format specified:

                1. ADD_ROLE {{role_name}} - When a user wants to add a role to themselves
                   Example: If user says "Can I get the Gamer role?", respond with "ADD_ROLE Gamer"

                2. REMOVE_ROLE {{role_name}} - When a user wants to remove a role from themselves
                   Example: If user says "Please remove my Admin role", respond with "REMOVE_ROLE Admin"

                3. CHANGE_NICKNAME {{new_nickname}} - When a user wants to change their nickname
                   Example: If user says "Change my name to CoolUser", respond with "CHANGE_NICKNAME CoolUser"

                If the user's request doesn't match any of these commands, respond conversationally as a helpful assistant. Do not explain the commands or your reasoning process in your response.

                USER PROMPT: {prompt}
            """
        }]

        response = ollama.chat(model="gemma3:12b", messages=all_messages)
        return response["message"]["content"]