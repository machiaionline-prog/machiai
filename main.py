from fastapi import FastAPI, Request
from ai_engine import generate_reply
from database import get_user_style
from instagram_api import send_instagram
from config import VERIFY_TOKEN

app = FastAPI()

BUSY_USERS = {}

@app.get("/webhook")
def verify(hub_mode:str=None, hub_challenge:str=None, hub_verify_token:str=None):

    if hub_verify_token == VERIFY_TOKEN:
        return hub_challenge

    return "verification failed"


@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    try:

        message = data["entry"][0]["messaging"][0]["message"]["text"]

        user = data["entry"][0]["messaging"][0]["sender"]["id"]

        style = get_user_style(user)

        reply = generate_reply(message, style)

        send_instagram(user, reply)

    except Exception as e:
        print(e)

    return {"ok":True}
