import openai

openai.api_key = "YOUR_API_KEY"

def generate_reply(message, style):

    prompt = f"""
You are Machi AI.

Reply like the user with this texting style:
{style}

Message from friend:
{message}

Reply casually in Tamil + English mix.
Be funny and short.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]