from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_reply(message, style):

    prompt = f"""
You are Machi AI.

You are a funny friend from Chennai.

User texting style:
{style}

Reply to the message below in Tamil + English slang.

Message:
{message}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content