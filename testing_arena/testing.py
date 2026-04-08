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

# Example usage
example_caption = "this text is test for text position of the top templates and their sizes if this works i am the best codder ever 1 2 3 4 5 6 7 8 9 0 11 22 33 44 55 66 77"
example_image_path = "templates\\thor_heros1.jpg" 
tmple= {
    "id": "thor_heros.jpg",
    "tags": ["hero", "duty", "responsibility", "avengers", "thor"],
    "caption_style": "single-caption",
    "description": "Thor from Avengers saying 'Because that's what heroes do'. Used to justify a heroic or dutiful action, often with a hint of self-sacrifice or expected behavior.",
    "text": "top"
  }
render_caption_on_template(example_image_path, example_caption,tmple)
image = Image.open("C:\\Users\\ratan\\OneDrive\\Desktop\\meme-bot\\output_meme.jpg")
image.show()