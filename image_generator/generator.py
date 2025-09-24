
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")

class GeminiImageGenerator:
    def __init__(self, api_key: str = API_KEY):
        self.client = genai.Client(api_key=api_key)

    def generate_meme(self, prompt: str, output_file: str = "generated_image.png"):
        """
        Generate a high-quality 16:9 meme image using Gemini AI.
        
        :param prompt: The prompt describing the meme.
        :param output_file: Path to save the generated image.
        :return: Path of the saved image.
        """
        response = self.client.models.generate_content(
            # Use the newer, non-deprecated model for image generation
            model="gemini-2.0-flash-preview-image-generation",
            contents=[prompt],
            config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"]
            ),

        )

        image_generated = False
        for part in response.candidates[0].content.parts:
            # Handle the mandatory text part of the response
            if part.text is not None:
                print(f"Text from model: {part.text}")
            # Process the image part
            elif part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                image.save(output_file)
                image_generated = True

        if image_generated:
            return output_file
        else:
            raise Exception("Failed to generate image from Gemini AI.")
