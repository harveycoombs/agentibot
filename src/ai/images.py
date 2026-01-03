from google import genai
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

google_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_image(prompt: str, output_path: str) -> Image:
    response = google_client.generate_image(
        model="gemini-2.5-flash-image",
        contents=[prompt]
    )

    for part in response.parts:
        if part.text is not None:
            return part.text
        elif part.inline_data is not None:
            image = part.as_image()
            image.save(output_path)

            return output_path