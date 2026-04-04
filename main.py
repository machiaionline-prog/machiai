import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

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

    if "messages" in data["entry"][0]["changes"][0]["value"]:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        from_number = msg["from"]
        text = msg["text"]["body"]

        send_whatsapp_message(from_number, f"You said: {text}")

    return {"status": "ok"}


def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {
            "body": message,
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    print("SEND STATUS:", response.status_code)
    print("SEND RESPONSE:", response.text)
