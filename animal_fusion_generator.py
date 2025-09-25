import random
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

# List of 50+ animals for fusion
ANIMALS = [
    "bunny", "kitten", "puppy", "panda", "fox", "owl", "hedgehog", "koala", "squirrel",
    "elephant", "lion", "tiger", "giraffe", "deer", "raccoon", "penguin", "seal",
    "dolphin", "whale", "horse", "donkey", "monkey", "otter", "hamster", "guinea pig",
    "parrot", "chick", "duck", "frog", "turtle", "llama", "alpaca", "cheetah",
    "zebra", "kangaroo", "platypus", "sloth", "lemur", "beaver", "moose", "wolf",
    "coyote", "bat", "skunk", "ferret", "peacock", "flamingo", "toucan", "swan"
]

# Prompt template for fusion
FUSION_PROMPT_TEMPLATE = (
    "A hyper-realistic 4K ultra HD wallpaper of an adorable fusion of a {Animal1} and a {Animal2}, "
    "softly glowing with elegance and charm. The creature should appear in a dreamy {Background} with pastel tones, "
    "gentle golden light, and a soft-focus background. The design should be soothing, elegant, balanced in composition, "
    "highly detailed, and perfect for a phone wallpaper — irresistibly cute with an elegant aesthetic."
)

# Backgrounds mapping based on animals
BACKGROUND_MAPPING = {
    "bunny": "flower meadow",
    "kitten": "cozy blanket with soft sunlight",
    "puppy": "grassy field with daisies",
    "panda": "bamboo forest with soft mist",
    "fox": "autumn leaves with golden sunlight",
    "owl": "moonlit forest with glowing fireflies",
    "default": "soft natural scenery"
}


def get_random_animals(count=2):
    """Return a list of random animals for fusion."""
    return random.sample(ANIMALS, count)


def get_background_for_animal(animal: str):
    """Return background based on animal or default."""
    for key in BACKGROUND_MAPPING:
        if key in animal.lower():
            return BACKGROUND_MAPPING[key]
    return BACKGROUND_MAPPING["default"]


def generate_fusion_prompt(animal1: str, animal2: str):
    """Generate JSON prompt for fusion of two animals."""
    # Pick background based on first animal, fallback to second
    background = get_background_for_animal(animal1)
    if background == BACKGROUND_MAPPING["default"]:
        background = get_background_for_animal(animal2)

    prompt_text = FUSION_PROMPT_TEMPLATE.format(Animal1=animal1, Animal2=animal2, Background=background)
    return {
        "Animals": [animal1, animal2],
        "Prompt": prompt_text,
        "Style": "Hyper-realistic, dreamy, elegant, pastel tones",
        "Quality": "4K Ultra HD",
        "Ratio": "9:16"
    }
