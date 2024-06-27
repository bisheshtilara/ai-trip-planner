import requests
import spacy
from helper.translate import translate_text
from model.get_origin_destination import get_origin_destination

# Function to scrape the data
def get_entities(text, language_code):
    try:
        translated_text = text
        # Translate the text to French
        if language_code == "en-EN":
            translated_text = translate_text(text, "en", "fr")
            print(f"Translated text: {translated_text}")

        result = get_origin_destination(translated_text)
        
        if result is not None:
            return result
        else:
            print(f"Invalid input structure. Unable to extract entities.")
            raise ValueError("Invalid input structure. Unable to extract entities.")
    except Exception as e:
        print("nlp: An error occurred:", str(e))
        return "nlp: An error occurred: {}".format(str(e))
