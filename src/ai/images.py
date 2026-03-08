from google import genai
from PIL import Image
import os

google_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_image(prompt: str, output_path: str) -> Image:
    response = google_client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt
    )

    for part in response.parts:
        if part.inline_data:
            image = part.as_image()
            image.save(output_path)