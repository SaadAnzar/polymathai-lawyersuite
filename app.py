from fastapi import FastAPI
import json
from db_supabase import create_supabase_client
from extract_text import extract_text
from generate_response import get_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

supabase = create_supabase_client()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Greetings": "Welcome Polymath user!"}


@app.post("/extract-and-generate")
async def extract_and_generate(matterid: str):
    try:
        matter = supabase.table("Matter").select("files").eq("id", matterid).execute()

        content = extract_text(files=matter.data[0]["files"])

        response = get_response(content=content)

        content_str = json.dumps(content)

        matter_update = (
            supabase.table("Matter")
            .update({"extractedText": content_str, "response": response})
            .eq("id", matterid)
            .execute()
        )

        print("Added to supabase successfully!")
        return {"status": "Added to supabase successfully!"}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"status": f"There is an error {e}"}
