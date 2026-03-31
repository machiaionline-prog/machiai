from database.mongodb import learning


def extract_style_patterns(messages):
    slang_words = [
        "machi",
        "bro",
        "dei",
        "da",
        "lol",
        "haha",
        "seri",
    ]

    found = []

    for message in messages:
        for word in slang_words:
            if word in message.lower():
                found.append(word)

    return list(set(found))


def update_user_style(user, patterns):
    learning.update_one(
        {"user": user},
        {"$set": {"style": patterns}},
        upsert=True,
    )
