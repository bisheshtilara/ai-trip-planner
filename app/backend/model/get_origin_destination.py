import spacy
from .train_model import train_model

version = 1
with open("./model/version.txt", "r") as f:
    version = int(f.read())
    f.close()

#Check if the model exists
try:
    nlp = spacy.load(f"./model/trained_model-v{version}")
except:
    train_model()
    version += 1
    nlp = spacy.load(f"./model/trained_model-v{version}")

def detect_french_entities(text):
    # Load spaCy model
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(text)

    # Extract entities
    ents = [ent.text for ent in doc.ents if ent.label_ == 'LOC']

    if len(ents) == 0:
        return None
    return ents[0]

def get_origin_destination(text):
    doc = nlp(text)

    places = [token.text for token in doc if token.dep_ == 'PLACE']
    ents = []

    for place in places:
        ent = detect_french_entities(place)
        if ent:
            ents.append(ent)

    revert = any(token.dep_ == 'REVERT' for token in doc)

    if len(ents) != 2:
        return {'origin': None, 'destination': None, 'entities': ents}

    if revert:
        # Swap origin and destination
        ents = ents[::-1]
    return {'origin': ents[0], 'destination': ents[1]}
