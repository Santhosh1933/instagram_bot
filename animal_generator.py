import random
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

# List of 100+ animals
ANIMALS = [
    "bunny", "kitten", "puppy", "panda", "fox", "owl", "hedgehog", "koala", "squirrel",
    "baby elephant", "baby lion", "baby tiger", "baby giraffe", "baby deer", "baby raccoon",
    "baby penguin", "baby seal", "baby dolphin", "baby whale", "baby horse", "baby donkey",
    "baby monkey", "baby otter", "baby hamster", "baby guinea pig", "baby parrot", "baby chick",
    "baby duck", "baby frog", "baby turtle", "baby hedgehog", "baby llama", "baby alpaca",
    "baby cheetah", "baby zebra", "baby kangaroo", "baby platypus", "baby sloth", "baby lemur",
    "baby beaver", "baby moose", "baby wolf", "baby coyote", "baby bat", "baby skunk", "baby ferret",
    "baby owl", "baby crow", "baby raven", "baby peacock", "baby flamingo", "baby toucan",
    "baby swan", "baby goose", "baby parakeet", "baby canary", "baby chickadee", "baby finch",
    "baby goldfish", "baby koi", "baby seahorse", "baby crab", "baby starfish", "baby jellyfish",
    "baby octopus", "baby squid", "baby lionfish", "baby axolotl", "baby tarantula", "baby scorpion",
    "baby butterfly", "baby ladybug", "baby dragonfly", "baby snail", "baby rabbit", "baby cat",
    "baby dog", "baby bear", "baby raccoon", "baby skunk", "baby goat", "baby sheep", "baby cow",
    "baby pig", "baby chicken", "baby turkey", "baby owl", "baby hawk", "baby eagle", "baby falcon",
    "baby iguana", "baby chameleon", "baby snake", "baby frog", "baby toad"
]

# Template for prompt
PROMPT_TEMPLATE = (
    "A hyper-realistic 4K ultra HD wallpaper of an adorable baby {Animal}, softly glowing with elegance and charm. "
    "The {Animal} should appear in a dreamy {Background} with pastel tones, gentle golden light, and a soft-focus background. "
    "The design should be soothing, elegant, balanced in composition, highly detailed, and perfect for a phone wallpaper — irresistibly cute with an elegant aesthetic."
)

# Backgrounds mapping based on animal type
BACKGROUND_MAPPING = {
    "bunny": "flower meadow",
    "kitten": "cozy blanket with soft sunlight",
    "puppy": "grassy field with daisies",
    "panda": "bamboo forest with soft mist",
    "fox": "autumn leaves with golden sunlight",
    "owl": "moonlit forest with glowing fireflies",
    "default": "soft natural scenery"
}


def get_random_animal():
    """Return a random animal from the list."""
    return random.choice(ANIMALS)


def get_background_for_animal(animal: str):
    """Return background based on animal or default."""
    for key in BACKGROUND_MAPPING:
        if key in animal.lower():
            return BACKGROUND_MAPPING[key]
    return BACKGROUND_MAPPING["default"]


def generate_prompt(animal: str):
    """Generate prompt JSON for the given animal."""
    background = get_background_for_animal(animal)
    prompt_text = PROMPT_TEMPLATE.format(Animal=animal, Background=background)
    return {
        "Animal": animal,
        "Prompt": prompt_text,
        "Style": "Hyper-realistic, dreamy, elegant, pastel tones",
        "Quality": "4K Ultra HD",
        "Ratio": "9:16"
    }


if __name__ == "__main__":
    animal = get_random_animal()
    prompt_json = generate_prompt(animal)
    print(prompt_json)
