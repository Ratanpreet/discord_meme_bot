import json, os
from PIL import Image, ImageDraw, ImageFont


# Load template metadata
with open("templates.json", "r") as f:
    template_db = json.load(f)

# Pick a template (example: the first one)
template = template_db[18]  

# Get full path to image
image_path = os.path.join("templates", template["id"])

# Open it
image = Image.open(image_path)
image.show()
