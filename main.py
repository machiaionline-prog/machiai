from fastapi import FastAPI,Request

from ai_engine.chat_ai import generate_reply
from fun_engine.roast_engine import roast
from fun_engine.meme_engine import random_meme
from business_engine.sales_bot import sales_reply

app = FastAPI()

@app.post("/webhook")

async def webhook(request:Request):

    data = await request.json()

    user = data["user"]
    message = data["message"]

    if "roast" in message:

        reply = roast()

    elif "meme" in message:

        reply = random_meme()

    else:

        business = sales_reply(message)

        if business:
            reply = business
        else:
            reply = generate_reply(message)

    return {"reply":reply}