from datetime import date
from dotenv import load_dotenv
from endpoints.nlp_input.route import router as nlp_input_router
from endpoints.nlp_voice.route import router as nlp_voice_router
from endpoints.path_finder.route import router as path_finder_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase.index import db
import os

load_dotenv()

app = FastAPI()

origins = [
    os.environ.get("ORIGIN"),
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nlp_input_router)
app.include_router(nlp_voice_router)
app.include_router(path_finder_router)

@app.get("/ping")
def ping():
    return {"message": "pong"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)