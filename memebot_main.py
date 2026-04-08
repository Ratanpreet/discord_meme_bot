# %%


# %%
import os
import json
from sentence_transformers import SentenceTransformer, util
from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import Image
import torch
import requests
import base64
# Load your template metadata
with open("templates.json", "r") as f:
    templates = json.load(f)


# %%
st_model = SentenceTransformer("all-MiniLM-L6-v2")
descs = [t["description"] + " " + " ".join(t["tags"]) for t in templates]
desc_embeddings = st_model.encode(descs, convert_to_tensor=True)


# %% twmplate selection
def select_template(prompt):
    pe = st_model.encode(prompt, convert_to_tensor=True)
    sims = util.cos_sim(pe, desc_embeddings)[0]
    idx = sims.argmax().item()
    tmpl = templates[idx]
    return os.path.join("templates", tmpl["id"]), tmpl


# %% caption generation
def generate_caption(image_path, prompt, template):
    # Read image as base64
    with open(image_path, "rb") as img_file:
        image_data = base64.b64encode(img_file.read()).decode("utf-8")

    # Construct contextual prompt
    context_prompt = f"""
Meme idea: {prompt}
Template description: {template['description']}
Tags: {', '.join(template['tags'])}
.
Generate a short, funny, and sarcastic meme caption for this template. Avoid literal explanations make sure that the context in the prompt is relavent to the caption.Dont mention characters that are in the templates use the propmt for caption.
"""

    # POST to LLaVA-
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llava:7b",
            "messages": [
                {"role": "system", "content": " Generate a short, funny, and highly shareable caption that fits the meme template based on the given context. Avoid being literal — go for irony, exaggeration, or punchline format most importantly be funny. dont explain the template.Make sure to use the prompt for the caption.Do not use emojis.Do not use hastags"},

                
                {"role": "user", "content": context_prompt}
            ],
            "images": [image_data],
            "stream": False
        }
    )

    response.raise_for_status()
    caption = response.json()["message"]["content"]
    return caption.strip()


# %%Image rendering
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def render_caption_on_template(image_path, caption_text,tmpl, output_path="output_meme.jpg"):
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    try:
        font_path = "arialbd.ttf"  # Windows bold font
        font = ImageFont.truetype(font_path, size=20)
    except:
        font = ImageFont.load_default()

    img_width, img_height = image.size

    # Wrap text
    margin = 0
    max_text_width = img_width - 2 * margin
    wrapper = textwrap.TextWrapper(width=45)
    wrapped_text = wrapper.fill(text=caption_text)

    # Get text size using textbbox
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    if tmpl['text']=='inside':

        x = (img_width - text_width) / 2
        y = img_height - text_height -20
    elif tmpl['text']== 'top':
        x = (img_width - text_width) / 2
        y=10
    else :
        print('fix ur code')
    # Draw black shadow
    shadow_offset = 2
    for dx in [-shadow_offset, shadow_offset]:
        for dy in [-shadow_offset, shadow_offset]:
            draw.text((x + dx, y + dy), wrapped_text, font=font, fill="black")

    # Draw white text
    draw.text((x, y), wrapped_text, font=font, fill="white")

    image.save(output_path)
    if tmpl['text'] == 'inside':
        print('inside')
    elif tmpl['text']=='top':
        print('top')
    else :
        print('idk what is wrong')


    print(f"Meme saved to: {output_path}")
    return output_path


# %%

#prompt = input("Enter your meme prompt: ")
#img_path, tmpl = select_template(prompt)
#print(prompt)
#print(img_path)
#print(tmpl)
#print("\n Using template:", tmpl["id"])
#print(" Tags:", ", ".join(tmpl["tags"]), "\n")

#caption = generate_caption(img_path, prompt, tmpl)

#print(" Generated Caption:", caption)
#render_caption_on_template(img_path, caption,tmpl)


#image = Image.open("C:\\Users\\ratan\\OneDrive\\Desktop\\meme-bot\\output_meme.jpg")
#image.show()


