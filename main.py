import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse

from ai_engine.chat_ai import generate_reply

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.get("/")
def home():
    return {"message": "Machi AI is running"}

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
    print(data)

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        sender_id = value["contacts"][0]["wa_id"]
        message = value["messages"][0]["text"]["body"]

        reply = generate_reply(message)
        WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
        PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

        url = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"

        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": sender_id,
            "text": {
                "body": reply,
            },
        }

        r = requests.post(url, headers=headers, json=payload)

        print(r.status_code)
        print(r.text)

        return {
            "status": "ok",
            "sender": sender_id,
            "message": message,
            "reply": reply,
        }

    except Exception as e:
        return {"error": str(e), "data": data}
