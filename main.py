from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse

from ai_engine.chat_ai import generate_reply
from fun_engine.roast_engine import roast
from fun_engine.meme_engine import random_meme
from business_engine.sales_bot import sales_reply

app = FastAPI()

VERIFY_TOKEN = "machi123"

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge)

    return PlainTextResponse("Forbidden", status_code=403)

@app.post("/webhook")
async def webhook(request: Request):

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

    return {"reply": reply}
