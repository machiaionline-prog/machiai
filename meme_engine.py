from PIL import Image, ImageDraw, ImageFont

def generate_meme(text):

    img = Image.new("RGB",(600,600),"white")

    draw = ImageDraw.Draw(img)

    draw.text((50,250),text,fill="black")

    path = "meme.png"

    img.save(path)

    return path