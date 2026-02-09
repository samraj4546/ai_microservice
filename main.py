from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class PRRequest(BaseModel):
    description: str


@app.get("/")
def home():
    return {"message": "AI Microservice Running"}


@app.post("/summarize")
def summarize_pr(pr: PRRequest):

    # ✅ Check if API key exists
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "error": "OpenAI API key not configured"
        }

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # safest + fastest model
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

    except Exception as e:
        # ✅ Prevents Internal Server Error
        return {
            "error": "OpenAI request failed",
            "details": str(e)
        }
