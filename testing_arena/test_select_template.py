import json
import os
from sentence_transformers import SentenceTransformer, util

TEMPLATE_FILE = "templates.json"
TEMPLATE_FOLDER = "templates"

# Load model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')

def select_template(prompt):
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        templates = json.load(f)

    # Embed the input prompt
    prompt_embedding = model.encode(prompt, convert_to_tensor=True)

    best_match = None
    best_score = -1

    for template in templates:
        # Combine tags + description into one searchable text
        template_text = " ".join(template["tags"]) + " " + template["description"]
        template_embedding = model.encode(template_text, convert_to_tensor=True)

        # Compute cosine similarity
        score = util.cos_sim(prompt_embedding, template_embedding).item()

        if score > best_score:
            best_score = score
            best_match = template

    return os.path.join(TEMPLATE_FOLDER, best_match["id"]), best_match

# Test it
if __name__ == "__main__":
    prompt = input("Enter your meme prompt: ")
    image_path, template = select_template(prompt)

    if image_path:
        print(f"\n✅ Selected Template: {template['id']}")
        print(f"📂 Image Path: {image_path}")
        print(f"🏷️ Tags: {', '.join(template['tags'])}")
    else:
        print("❌ No suitable template found.")
