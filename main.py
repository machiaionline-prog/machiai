from fastapi import FastAPI, Request
from ai_engine import generate_reply
from database import get_user_style
from whatsapp import send_whatsapp_message
from config import VERIFY_TOKEN

app = FastAPI()

BUSY_USERS = {}

@app.get("/webhook")
def verify(mode: str=None, challenge: str=None, verify_token: str=None):

    if verify_token == VERIFY_TOKEN:
        return challenge

    return "verification failed"


@app.post("/webhook")
async def receive_message(request: Request):

    data = await request.json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

        user = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]

        if user in BUSY_USERS:

            style = get_user_style(user)

            reply = generate_reply(message, style)

            send_whatsapp_message(user, reply)

    except Exception as e:
        print(e)

    return {"status":"ok"}