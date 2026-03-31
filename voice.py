from gtts import gTTS
import uuid

def generate_voice(text):

    filename=f"voice_{uuid.uuid4()}.mp3"

    tts=gTTS(text=text,lang="ta")

    tts.save(filename)

    return filename