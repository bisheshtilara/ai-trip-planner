from fastapi import APIRouter
from pydantic import BaseModel
from .controller import process_base64_audio
from ..nlp_input.controller import get_entities
from dotenv import load_dotenv
import os
import base64

load_dotenv()

router = APIRouter()

class VoiceInput(BaseModel):
    file_content: str
    language_code: str

@router.post("/voice")
def get_nlp(data: VoiceInput):
    input_voice = process_base64_audio(data.file_content, data.language_code)
    try:
        result = get_entities(input_voice, data.language_code)

        code_status = 200
        
        if type(result) == str:
            code_status = 400

        return {"message": "POST nlp voice", "nlp": result, "input_voice": input_voice,  "code_status": code_status}
    except Exception as e:
        return {"message": "POST nlp voice", "nlp": {}, "input_voice": input_voice, "code_status": 404, "error": str(e)}
