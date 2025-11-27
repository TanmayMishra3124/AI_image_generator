import os
import json
import datetime
from PIL import Image, ImageDraw, ImageFont

# --- Safety Filter ---
RESTRICTED_KEYWORDS = [
    "nsfw", "nude","naked","sex",  "porn", "erotic", "hentai",
    "violence", "blood", "gore", "kill", "murder", "suicide", "torture",
    "hate", "racist", "nazi", "fascist", "supremacist", "slur",
    "child abuse", "pedophile", "underage", "lolita",
    "drugs", "cocaine", "heroin", "meth",
    "terrorist", "bomb", "explosion", "weapon",
    "deepfake", "fake news", "disinformation"
]

# Default Negative Prompt for Safety & Quality
DEFAULT_NEGATIVE_PROMPT = "nsfw, nude, naked, porn, ugly, deformed, bad anatomy, blurry, low quality, topless, nipples, cleavage, uncensored, skin, explicit, poorly drawn face, mutation, mutated, extra limb, poorly drawn hands, missing limb, floating limbs, disconnected limbs, malformed hands, out of focus, long neck, long body"

def check_safety(prompt):
    """
    Checks if the prompt contains any restricted keywords.
    Returns (is_safe, reason).
    """
    prompt_lower = prompt.lower()
    for keyword in RESTRICTED_KEYWORDS:
        if keyword in prompt_lower:
            return False, f"Restricted keyword detected: '{keyword}'"
    return True, "Safe"

# --- Prompt Engineering ---
STYLE_PRESETS = {
    "Photorealistic": "highly detailed, 4K, ultra-sharp, cinematic lighting, professional photography, 8k resolution",
    "Artistic": "digital art, trending on artstation, creative, expressive, vivid colors",
    "Cartoon": "cartoon style, vibrant, flat colors, clean lines",
    "Anime": "anime style, studio ghibli, makoto shinkai, detailed background",
    "Van Gogh": "oil painting, post-impressionist, thick brush strokes, starry night style, van gogh"
}

def enhance_prompt(user_prompt, style_preference):
    """
    Enhances the user prompt with style descriptors.
    """
    enhanced_prompt = user_prompt
    if style_preference in STYLE_PRESETS:
        enhanced_prompt += f", {STYLE_PRESETS[style_preference]}"
    
    # General quality boosters
    enhanced_prompt += ", high quality, masterpiece"
    return enhanced_prompt

# --- Watermarking ---
def add_watermark(image, text="AI-generated"):
    """
    Adds a text watermark to the bottom right corner of the image.
    """
    # Create a copy to avoid modifying the original
    watermarked_image = image.copy()
    draw = ImageDraw.Draw(watermarked_image)
    
    # Try to load a default font, fallback to default if not available
    try:
        # Using a larger font size if possible, but default is fine for basic
        font = ImageFont.truetype("Arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size and position
    # textbbox is available in newer Pillow versions, textsize is deprecated
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback for older Pillow versions
        text_width, text_height = draw.textsize(text, font=font)

    width, height = watermarked_image.size
    x = width - text_width - 10
    y = height - text_height - 10

    # Draw text with a slight shadow for visibility
    draw.text((x+1, y+1), text, font=font, fill="black")
    draw.text((x, y), text, font=font, fill="white")
    
    return watermarked_image

# --- Storage ---
def save_image_and_metadata(image, prompt, params, output_dir="outputs", filename_prefix="image"):
    """
    Saves the image and its metadata to a timestamped directory.
    """
    # Create timestamped directory
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = os.path.join(output_dir, datetime.datetime.now().strftime("%Y-%m-%d"), f"{timestamp}_run")
    os.makedirs(run_dir, exist_ok=True)

    # Save Image
    image_filename = f"{filename_prefix}.png"
    image_path = os.path.join(run_dir, image_filename)
    image.save(image_path)
    
    # Also save as JPG
    image_jpg_filename = f"{filename_prefix}.jpg"
    image_jpg_path = os.path.join(run_dir, image_jpg_filename)
    image.convert("RGB").save(image_jpg_path)

    # Save Metadata
    metadata = {
        "prompt": prompt,
        "timestamp": timestamp,
        "parameters": params
    }
    metadata_path = os.path.join(run_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)

    return run_dir, image_path, image_jpg_path
