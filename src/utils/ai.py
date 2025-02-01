import ollama

class AI:
    @staticmethod
    async def generate_text_response(messages, model="deepseek-v2:lite"):
        context = [{
            "role": "user",
            "content": ""
        }]

        response = ollama.chat(model=model, messages=context)
        return response["message"]["content"]