import requests
from config import WHATSAPP_TOKEN, PHONE_NUMBER_ID

def send_whatsapp_message(user, text):

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": user,
        "text": {"body": text}
    }

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    requests.post(url, json=payload, headers=headers)