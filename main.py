from typing import List
from pydantic import BaseModel
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from extract_text import extract_text
from generate_response import get_response

app = FastAPI()


# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    key: str
    url: str
    name: str


@app.get("/")
async def read_root():
    return {"Greetings": "Welcome Polymath user!"}


@app.post("/extract-and-generate")
async def extract_and_generate(files: List[Item]):
    try:
        print(files)

        content = extract_text(files=files)

        response = get_response(content=content)

        content_str = json.dumps(content)

        # print("extractedText:", content_str)
        # print("response", response)
        return {"extractedText": content_str, "response": response}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"status": f"There is an error, {e}"}
