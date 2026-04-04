import os

from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse

from ai_engine.chat_ai import generate_reply
from integrations.whatsapp_api import send_whatsapp_message

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
        incoming_message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        message = incoming_message["text"]["body"]
        from_number = incoming_message["from"]

        reply = generate_reply(message)
        send_whatsapp_message(from_number, reply)

        return {
            "status": "ok",
            "sender": from_number,
            "message": message,
            "reply": reply,
        }

    except Exception as e:
        return {"error": str(e), "data": data}
