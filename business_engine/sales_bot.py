def sales_reply(message):

    if "price" in message.lower():

        return "Product price ₹499. Delivery available."

    if "book" in message.lower():

        return "Please share your name and preferred time."

    return None