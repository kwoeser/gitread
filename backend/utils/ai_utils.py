import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def generate_readme_with_gemini(prompt):
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Gemini API error: {response.text}")
    
    result = response.json()
    candidates = result.get("candidates")
    if candidates and len(candidates) > 0:
        generated_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text")
    else:
        generated_text = None
    return generated_text
