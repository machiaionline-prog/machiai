from urllib.parse import quote
import uuid

import requests
from openai import OpenAI

from config.settings import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_meme_text(user_message):
    prompt = f"""
Create a funny Tamil meme text in Tanglish.

User message: {user_message}

Format:
TOP TEXT:
BOTTOM TEXT:
""".strip()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def create_meme_image(text):
    top_text = "_"
    bottom_text = "_"

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines:
        upper_line = line.upper()
        if upper_line.startswith("TOP TEXT:"):
            top_text = line.split(":", 1)[1].strip() or "_"
        elif upper_line.startswith("BOTTOM TEXT:"):
            bottom_text = line.split(":", 1)[1].strip() or "_"

    if top_text == "_" and bottom_text == "_" and text.strip():
        bottom_text = text.strip()

    meme_api = "https://api.memegen.link/images/drake"
    url = f"{meme_api}/{quote(top_text, safe='')}/{quote(bottom_text, safe='')}.png"
    filename = f"meme_{uuid.uuid4()}.png"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    with open(filename, "wb") as file_obj:
        file_obj.write(response.content)

    return filename
