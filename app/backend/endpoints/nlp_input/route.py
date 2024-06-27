from fastapi import APIRouter
from pydantic import BaseModel
from .controller import get_entities
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

class TextInput(BaseModel):
    text: str
    language_code: str

@router.post("/input")
def get_nlp(text_input: TextInput):
    try:
        result = get_entities(text_input.text, text_input.language_code)
        return {"message": "POST nlp input", "nlp": result, "code_status": 200}
    except Exception as e:
        return {"message": "POST nlp input", "nlp": {}, "code_status": 404}