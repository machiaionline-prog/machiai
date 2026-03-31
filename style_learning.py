from database.mongodb import db

def learn_style(user):

    messages=list(db.messages.find({"user":user}).limit(20))

    style=""

    for m in messages:
        style+=m["message"]+"\n"

    return style
