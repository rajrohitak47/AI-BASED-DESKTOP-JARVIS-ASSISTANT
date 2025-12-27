from googletrans import Translator

translator = Translator()

def translate_to_english(text):
    translated = translator.translate(text, dest='en')
    return translated.text
