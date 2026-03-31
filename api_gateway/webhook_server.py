from fastapi import FastAPI, Request

from ai_engine.chat_ai import generate_reply
from database.mongodb import messages, save_message
from fun_engine.meme_engine import create_meme_image, generate_meme_text
from fun_engine.roast_engine import get_roast
from integrations.instagram_api import send_instagram_image, send_instagram_message
from integrations.whatsapp_api import send_whatsapp_message
from learning_engine.style_learning import extract_style_patterns, update_user_style
from voice import generate_voice

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        user = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
        platform = data["entry"][0]["changes"][0]["value"]["messaging_product"]

        save_message(user, message)

        history = list(messages.find({"user": user}).limit(20))
        texts = [item["message"] for item in history]
        patterns = extract_style_patterns(texts)
        update_user_style(user, patterns)

        message_text = message.lower()

        if platform == "instagram" and "meme" in message_text:
            meme_text = generate_meme_text(message)
            meme_file = create_meme_image(meme_text)
            send_instagram_image(user, meme_file)
            return {"status": "ok"}

        if platform == "instagram" and "roast" in message_text:
            send_instagram_message(user, get_roast())
            return {"status": "ok"}

        reply = generate_reply(user, message)

        if "voice" in message_text:
            generate_voice(reply)

        if platform == "whatsapp":
            send_whatsapp_message(user, reply)
        elif platform == "instagram":
            send_instagram_message(user, reply)

    except Exception as exc:
        print(exc)

    return {"status": "ok"}
