from openai import OpenAI

client = OpenAI()

def generate_response_to_image(model, prompt, attachment_url):
    if model.startswith("gpt-"):
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
    else:
        return ""