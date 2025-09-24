
from google import genai
from google.genai import types
import random
import time
from constants import API_KEY

FLAGS = [
    "js meme", "developer life", "python memory leak", "debugging chaos",
    "frontend struggle", "backend server crash", "git merge conflict",
    "coffee fueled coding", "rubber duck debugging", "AI assistant fail"
]

class GeminiPromptGenerator:
    def __init__(self, api_key: str = API_KEY, max_retries: int = 5, backoff_factor: int = 2):
        self.client = genai.Client(api_key=api_key)
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def generate_creative_prompt(self, flag: str) -> str:
        """
        Use Gemini AI to generate a high-quality meme prompt dynamically.
        Retries automatically if Gemini API is overloaded.
        """
        ai_prompt = (
            f"Generate a creative, funny, absurd 16:9 programming meme prompt "
            f"based on this idea: '{flag}'. "
            f"The prompt should describe the scene, the characters, the chaos, "
            f"a humorous caption at the bottom, and visual style details "
            f"(vibrant colors, cartoonish, exaggerated expressions, dynamic lighting). "
            f"Return only the meme prompt text."
        )

        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=[ai_prompt],
                    config=types.GenerateContentConfig(response_modalities=["TEXT"])
                )

                for part in response.candidates[0].content.parts:
                    if part.text:
                        return part.text.strip()

                raise Exception("No text returned from Gemini API")

            except Exception as e:
                wait_time = self.backoff_factor ** attempt
                print(f"[Retry {attempt+1}/{self.max_retries}] Gemini API failed: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)

        raise Exception("Max retries reached. Gemini API is unavailable. Try again later.")

    def get_random_flag(self):
        return random.choice(FLAGS)
