import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Retrieve the API key from the environment


"""
Possible endpoints

- generate_readme(): 
    receives data and then returns the generated text
    creates the readme 

- health():
    check if the app is running 
"""

print("API Key:", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/generate_readme', methods=["POST"])
def generate_readme():
    data = request.get_json()

    if not data or "repository_data" not in data:
        return jsonify({"error": "Missing repository data"}), 400

    repository_data = data.get("repository_data")
    prompt = (
        f"Generate a detailed README file for a GitHub repository with the following information:\n\n"
        f"{repository_data}\n\n"
        "Include sections such as Overview, Installation, Usage, Contributing, and License."
    )

    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes clear and detailed README files."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500)
        generated_text = response.choices[0].message.content
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"README": generated_text})

@app.route('/health', methods=["GET"])
def health():
    return jsonify({"message": "App is running and health endpoint is good"})

if __name__ == "__main__":
    app.run(debug=True)
