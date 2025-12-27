from gtts import gTTS
from playsound import playsound
import os
import random

def speak(text):
    print(f"Jarvis: {text}")  # 🖨️ Print the text

    tts = gTTS(text=text, lang='en')
    filename = f"voice_{random.randint(1,10000)}.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)
