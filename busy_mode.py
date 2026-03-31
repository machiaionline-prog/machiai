from database.mongodb import db

def enable_busy(user):

    db.busy.update_one(
        {"user":user},
        {"$set":{"status":True}},
        upsert=True
    )

def disable_busy(user):

    db.busy.update_one(
        {"user":user},
        {"$set":{"status":False}}
    )

def is_busy(user):

    data=db.busy.find_one({"user":user})

    if data and data["status"]:
        return True

    return False
