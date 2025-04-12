import ollama

class AI:
    @staticmethod
    def format_message(message):
        return {
            "role": "user",
            "content": message.content
        }

    @staticmethod
    async def generate_text_response(messages, model="deepseek-v2:lite"):
        context = map(AI.format_message, messages)

        response = ollama.chat(model=model, messages=context)
        return response["message"]["content"]
    
    
    @staticmethod
    async def respond_to_command(prompt):
        response = ollama.chat(model="gemma3:12b", messages=[{
            "role": "user",
            "content": f"FYI, you were created by somebody called Harvey. I am going to give you the following key: 'ADD_ROLE {{name}}' = the user wants to add a specific role to themselves, by providing the name of it. 'REMOVE_ROLE {{name}}' = the user wants to remove a specific role from themselves, by providing the name of it. 'CHANGE_NICKNAME {{name}}' = the user wants to change their nickname to the name provided. Please only reply with the command and make sure to substitute the '{{name}}' placeholder with the name of the role they have provided. If you cannot match up the user's prompt with an existing command, respond to their prompt as you normally would. With that being said, here is the user's prompt: {prompt}",
        }])

        return response["message"]["content"]