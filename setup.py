from setuptools import setup, find_packages

setup(
    name='instagram_bot',
    version='0.1.0',
    packages=find_packages(include=[
        'image_generator',
        'instagram_uploader',
        'flashcard_generator',
        'meme_prompt_generator'
    ]),
    # ... other arguments ...
)