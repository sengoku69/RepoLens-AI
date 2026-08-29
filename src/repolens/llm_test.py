import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set.")

if not base_url:
    raise RuntimeError("OPENAI_BASE_URL is not set.")

if not model:
    raise RuntimeError("OPENAI_MODEL is not set.")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": (
                "You are testing the RepoLens AI project. "
                "Reply with exactly: RepoLens connection successful."
            ),
        }
    ],
)

print(response.choices[0].message.content)