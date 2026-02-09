from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class PRRequest(BaseModel):
    description: str


@app.get("/")
def home():
    return {"message": "AI Microservice Running"}


@app.post("/summarize")
def summarize_pr(pr: PRRequest):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this pull request in 3 bullet points:\n{pr.description}"
            }
        ],
        temperature=0.3
    )

    return {
        "summary": response.choices[0].message.content
    }
