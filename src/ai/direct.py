import os
from openai import OpenAI

from exception import VesperException

openai_client = OpenAI()
xai_client = OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")
gemini_client = OpenAI(api_key=os.getenv("GOOGLE_API_KEY"), base_url="https://generativelanguage.googleapis.com/v1beta/openai")
anthropic_client = OpenAI(api_key=os.getenv("ANTHROPIC_API_KEY"), base_url="https://api.anthropic.com/v1")

def generate_response_to_image(model, prompt, attachment_url):
    client = openai_client if model.startswith("gpt-") else xai_client if model.startswith("grok-") else gemini_client if model.startswith("gemini-") else anthropic_client if model.startswith("claude-") else None

    if not client:
        raise VesperException(f"Unable to determine provided model '{model}'.")

    response = client.responses.create(
        model=model,
        input=[{
            "role": "user", 
            "content": [{
                "type": "input_text", 
                "text": prompt 
            }, 
            { 
                "type": "input_image", 
                "image_url": attachment_url 
            }]
        }]
    )

    return response.output_text