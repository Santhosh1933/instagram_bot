import cloudinary
import cloudinary.uploader
from image_generator import GeminiImageGenerator
from instagram_uploader import InstagramUploader
from meme_prompt_generator import GeminiPromptGenerator
from constants import API_KEY, ACCESS_TOKEN, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, BUSINESS_ACCOUNT_ID

# Configure Cloudinary
cloudinary.config(
    cloud_name="dplmrowbo",
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

CAPTION = "#ProgrammingMeme #DevLife #CodingHumor #ProgrammerLife #Meme"

if __name__ == "__main__":
    generator = GeminiImageGenerator(API_KEY)
    local_file = "programming_meme.png"
    prompt_generator = GeminiPromptGenerator(API_KEY)

    # Step 0: Generate dynamic prompt
    flag = prompt_generator.get_random_flag()
    PROMPT = prompt_generator.generate_creative_prompt(flag)
    print("Generated Prompt:\n", PROMPT)

    # Step 1: Generate Meme
    try:
        generator.generate_meme(PROMPT, output_file=local_file)
        print(f"Meme image saved locally: {local_file}")
    except Exception as e:
        print("❌ Failed to generate meme:", e)
        exit(1)

    # Step 2: Upload to Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(local_file, folder="programming_memes")
        image_url = upload_result["secure_url"]
        public_id = upload_result["public_id"]
        print(f"✅ Image uploaded to Cloudinary: {image_url}")
    except Exception as e:
        print("❌ Failed to upload image to Cloudinary:", e)
        exit(1)

    # Step 3: Upload to Instagram
    uploader = InstagramUploader(ACCESS_TOKEN, BUSINESS_ACCOUNT_ID)
    try:
        success = uploader.upload_image(image_url, CAPTION)
        if success:
            print("✅ Image uploaded to Instagram successfully!")

            # Step 4: Delete image from Cloudinary to save space
            try:
                cloudinary.uploader.destroy(public_id)
                print("🗑️ Image deleted from Cloudinary successfully.")
            except Exception as e:
                print("⚠️ Failed to delete image from Cloudinary:", e)

    except Exception as e:
        print("❌ Failed to upload to Instagram:", e)
