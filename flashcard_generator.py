# flashcard_generator.py
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import time
import os
API_KEY = os.getenv("API_KEY")

class FlashcardGenerator:
    def __init__(self, api_key: str = API_KEY, max_retries: int = 5, backoff_factor: int = 2):
        self.client = genai.Client(api_key=api_key)
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def generate_flashcard_text(self, topic: str) -> dict:
        """
        Generate concise flashcard text: definition + example.
        Tries gemini-2.5-flash-lite first, falls back to gemini-2.0-flash if needed.
        """
        ai_prompt = (
            f"You are a flashcard creator for programmers and developers.\n"
            f"Create a flashcard on the topic: {topic}\n\n"
            f"Format the answer exactly as:\n"
            f"Short Definition: ...\n"
            f"Make it concise, beginner-friendly, and suitable for quick revision."
        )

        models_to_try = ["gemini-2.5-flash-lite", "gemini-2.0-flash"]
        last_exception = None
        for model_name in models_to_try:
            for attempt in range(self.max_retries):
                try:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=[ai_prompt],
                        config=types.GenerateContentConfig(response_modalities=["TEXT"])
                    )

                    text_output = ""
                    if response.candidates:
                        for part in response.candidates[0].content.parts:
                            if part.text:
                                text_output += part.text.strip() + "\n"

                    if not text_output:
                        raise Exception("No flashcard explanation generated.")

                    # Parse definition and example
                    definition, example = "", ""
                    for line in text_output.splitlines():
                        if line.lower().startswith("short definition:"):
                            definition = line.split(":", 1)[1].strip()
                        elif line.lower().startswith("example:"):
                            example = line.split(":", 1)[1].strip()

                    return {"topic": topic, "definition": definition, "example": example}

                except Exception as e:
                    last_exception = e
                    wait_time = self.backoff_factor ** attempt
                    print(f"[Retry {attempt+1}/{self.max_retries}] Gemini API failed (model {model_name}): {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
            # If all retries for this model fail, try next model
        raise Exception(f"Max retries reached. Gemini API is unavailable. Last error: {last_exception}")

    def generate_flashcard_image(self, flashcard: dict, output_file="flashcard.png") -> str:
        """
        Generate a flashcard image using Gemini AI image generation.
        """
        prompt = (
            f"Create a 16:9 flashcard image for programmers.\n"
            f"Topic: {flashcard['topic']}\n"
            f"Definition: {flashcard['definition'] if flashcard['definition'] else 'No definition available.'}\n"
            f"Style: clean, minimal, visually appealing, programmer-friendly, readable text, soft colors."
        )

        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash-preview-image-generation",
                    contents=[prompt],
                    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
                )

                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        image = Image.open(BytesIO(part.inline_data.data))
                        image.save(output_file)
                        return output_file

                raise Exception("No image returned from Gemini API")

            except Exception as e:
                wait_time = self.backoff_factor ** attempt
                print(f"[Retry {attempt+1}/{self.max_retries}] Gemini API failed: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)

        raise Exception("Max retries reached. Gemini image API unavailable.")

