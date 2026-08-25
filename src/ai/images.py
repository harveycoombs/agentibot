from google import genai
from PIL import Image

def generate_image(api_key: str, prompt: str, output_path: str) -> Image:
     google_client = genai.Client(api_key=api_key)
     
     response = google_client.models.generate_content(
          model="gemini-2.5-flash-image",
          contents=prompt
     )
     
     for part in response.parts:
          if part.inline_data:
               image = part.as_image()
               image.save(output_path)