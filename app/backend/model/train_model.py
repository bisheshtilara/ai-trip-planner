import json
import spacy
from spacy.util import minibatch, compounding
from spacy.tokens import Doc
from spacy.training import Example
from spacy.symbols import ORTH
import random

def train_model():
    # Load training data from JSON file
    with open('./model/train_data.json', 'r') as f:
        TRAINING_DATA = json.load(f)

    # Load a blank French model
    nlp = spacy.blank('fr')

    # Add the parser to the pipeline
    parser = nlp.add_pipe('parser')

    # Add labels to the parser
    for _, annotations in TRAINING_DATA:
        for dep in annotations.get('deps', []):
            parser.add_label(dep)

    # Add special case rule
    special_case = [{ORTH: "-"}]
    nlp.tokenizer.add_special_case("-", special_case)

    special_case = [{ORTH: "à"}]
    nlp.tokenizer.add_special_case("à", special_case)

    # Get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'parser']

    # Only train parser
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()

        for itn in range(50):  # number of iterations
            random.shuffle(TRAINING_DATA)
            losses = {}

            # Batch up the examples using spaCy's minibatch
            batches = minibatch(TRAINING_DATA, size=compounding(4., 32., 1.001))
            # ...
            for batch in batches:
                texts, annotations = zip(*batch)
                docs = []
                for text in texts:
                    # Use the nlp object to tokenize the text
                    doc = nlp.make_doc(text)  # Use make_doc to only tokenize the text
                    docs.append(doc)

                examples = []
                for i in range(len(docs)):
                    doc = docs[i]
                    try:
                        example = Example.from_dict(doc, annotations[i])
                        examples.append(example)
                    except ValueError as e:
                        print(f"Skipping document due to error: {e}")

                nlp.update(examples, sgd=optimizer, losses=losses)

    # Save the trained model with version number and date
    version = 1
    with open("./model/version.txt", "r") as f:
        version = int(f.read())
        version += 1
        #write the new version number to file
        f = open("./model/version.txt", "w")
        f.write(str(version))
        f.close()

    nlp.to_disk(f"./model/trained_model-v{version}")