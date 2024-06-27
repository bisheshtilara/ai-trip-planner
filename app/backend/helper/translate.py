from googletrans import Translator

def translate_text(text, src, dest):
    translator = Translator()
    translated_text = translator.translate(text, src=src, dest=dest)
    return translated_text.text
