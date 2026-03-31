from openai import OpenAI
from config.settings import OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)

SYSTEM_PROMPT = """
You are Machi AI.
A funny Tamil friend.
Speak Tanglish and use humor.
"""

def generate_reply(message):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":message}
        ]
    )

    return response.choices[0].message.content