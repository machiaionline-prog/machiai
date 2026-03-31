def qualify_lead(message):
    return {
        "intent": "lead_qualification",
        "summary": message.strip(),
    }
