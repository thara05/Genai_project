!pip install google-generativeai gradio pillow
!apt-get install fonts-dejavu-core

from google.colab import files
files.upload()

import google.generativeai as genai
import gradio as gr
from PIL import Image, ImageDraw, ImageFont


genai.configure(api_key="AIzaSyABWFC-6qcMv9uXGMlQAWRWFNLizR2AafE")

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={
        "temperature": 0.7,
        "max_output_tokens":20
    }
)

def generate_ai_caption(prompt, tone):
    try:
        response = model.generate_content(
            f"Write a {tone} caption about {prompt} with 3 hashtags."
        )
        return response.text
    except Exception as e:
        return "AI generation failed"



def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))



def create_post(prompt, platform, tone, font_size, color):

    caption = generate_ai_caption(prompt, tone)

    
    if platform == "Instagram":
        img = Image.open("instagram.png").convert("RGB")
    elif platform == "LinkedIn":
        img = Image.open("linkedin.jpeg").convert("RGB")
    else:
        img = Image.open("quote.jpeg").convert("RGB")

    img = img.resize((800, 800))
    draw = ImageDraw.Draw(img)

    text = prompt.upper()

    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        int(font_size)
    )

  
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (800 - text_width) / 2
    y = (800 - text_height) / 2

    if color is None:
        rgb_color = (0, 0, 0)
    else:
        rgb_color = hex_to_rgb(color)

    draw.text((x, y), text, fill=rgb_color, font=font)

    return img, caption



def generate(prompt, platform, tone, font_size, color):
    image, caption = create_post(prompt, platform, tone, font_size, color)
    return image, caption



app = gr.Interface(
    fn=generate,
    inputs=[
        gr.Textbox(label="Enter Topic (Example: Education, AI, Success)"),
        gr.Dropdown(["Instagram", "LinkedIn", "Quote"], label="Select Platform"),
        gr.Dropdown(["Motivational", "Marketing", "Professional"], label="Select Tone"),
        gr.Slider(20, 80, value=40, label="Font Size"),
        gr.ColorPicker(label="Font Color")
    ],
    outputs=[
        gr.Image(label="Generated Social Media Post"),
        gr.Textbox(label="AI Generated Caption")
    ],
    title="🎨 AI-Powered Social Media Post Generator",
    description="This system uses Google Gemini (Generative AI) to dynamically generate captions."
)

app.launch()
