# ai_utils.py
import os
import requests
from dotenv import load_dotenv

# Ensure environment variables from .env are loaded
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
    print("Full Gemini Response:", result)  # Debug print

    # Attempt to extract the generated text
    candidates = result.get("candidates")
    if candidates and len(candidates) > 0:
        candidate = candidates[0]
        # Log candidate to inspect its structure
        print("Candidate extracted:", candidate)
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        if parts and len(parts) > 0:
            generated_text = parts[0].get("text")
        else:
            generated_text = None
    else:
        generated_text = None

    if not generated_text:
        # Fallback message if extraction failed
        generated_text = "No output returned from Gemini API."
    return generated_text

