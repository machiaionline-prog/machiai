import requests

from config.settings import PAGE_TOKEN


def send_instagram_message(user_id, text):
    url = "https://graph.facebook.com/v19.0/me/messages"
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE",
    }
    headers = {
        "Authorization": f"Bearer {PAGE_TOKEN}",
        "Content-Type": "application/json",
    }
    requests.post(url, json=payload, headers=headers, timeout=20)


def send_instagram_image(user_id, image_path):
    url = "https://graph.facebook.com/v19.0/me/messages"
    payload = {
        "recipient": '{"id":"' + user_id + '"}',
        "message": '{"attachment":{"type":"image","payload":{}}}',
        "messaging_type": "RESPONSE",
    }
    headers = {
        "Authorization": f"Bearer {PAGE_TOKEN}",
    }

    with open(image_path, "rb") as image_file:
        files = {"filedata": image_file}
        requests.post(url, data=payload, headers=headers, files=files, timeout=20)
