# animal_fusion_main.py

import os
import random
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

from animal_fusion_generator import generate_fusion_prompt, get_random_animals
from uploader import InstagramUploader  

load_dotenv()
API_KEY = os.getenv("API_KEY")
FUSED_ACCESS_TOKEN = os.getenv("FUSED_ACCESS_TOKEN")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
FUSED_BUSINESS_ACCOUNT_ID = os.getenv("FUSED_BUSINESS_ACCOUNT_ID")

# Configure Cloudinary
cloudinary.config(
    cloud_name="dplmrowbo",
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

CAPTION = "#CuteAnimals #PhoneWallpaper #AnimalFusion #ElegantAnimals"

if __name__ == "__main__":
    uploader = InstagramUploader(FUSED_ACCESS_TOKEN, FUSED_BUSINESS_ACCOUNT_ID)

    # Step 1: Pick random two animals
    animal1, animal2 = get_random_animals()
    prompt_data = generate_fusion_prompt(animal1, animal2)
    print("Generated Fusion Prompt for:", animal1, "and", animal2)
    print(prompt_data["Prompt"])

    # Step 2: Generate image using Gemini AI
    from google import genai
    from google.genai import types
    from PIL import Image
    from io import BytesIO
    import time

    client = genai.Client(api_key=API_KEY)

    local_file = f"{animal1}_{animal2}_fusion_wallpaper.png".replace(" ", "_")
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=[prompt_data["Prompt"]],
                config=types.GenerateContentConfig(response_modalities=["TEXT","IMAGE"])
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))
                    image.save(local_file)
                    print(f"✅ Image saved locally: {local_file}")
            break
        except Exception as e:
            wait_time = 2 ** attempt
            print(f"[Retry {attempt+1}] Gemini API failed: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
    else:
        raise Exception("Max retries reached. Failed to generate fusion image.")

    # Step 3: Upload to Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(local_file, folder="cute_animal_fusions")
        image_url = upload_result["secure_url"]
        public_id = upload_result["public_id"]
        print(f"✅ Image uploaded to Cloudinary: {image_url}")
    except Exception as e:
        print("❌ Failed to upload to Cloudinary:", e)
        exit(1)

    # Step 4: Upload to Instagram
    try:
        success = uploader.upload_image(image_url, f"{prompt_data['Prompt']} {CAPTION}")
        if success:
            print("✅ Fusion image uploaded to Instagram successfully!")

            # Step 5: Delete image from Cloudinary
            try:
                cloudinary.uploader.destroy(public_id)
                print("🗑️ Image deleted from Cloudinary successfully.")
            except Exception as e:
                print("⚠️ Failed to delete image from Cloudinary:", e)

    except Exception as e:
        print("❌ Failed to upload fusion image to Instagram:", e)
