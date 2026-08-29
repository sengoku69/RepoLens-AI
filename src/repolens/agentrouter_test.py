import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not loaded.")

url = f"{base_url}/models"

response = requests.get(
    url,
    headers={
        "Authorization": f"Bearer {api_key}",
    },
    timeout=30,
)

print("HTTP status:", response.status_code)
print("Response:", response.text[:2000])