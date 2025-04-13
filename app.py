# app.py
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from io import BytesIO

# Import our custom modules
from github_utils import get_repo_data, construct_prompt
from ai_utils import generate_readme_with_gemini

load_dotenv()

app = Flask(__name__)
CORS(app)

# Global variable to store the most recently generated README for demo purposes.
latest_readme = None

@app.route('/generate_readme_from_repo', methods=["POST"])
def generate_readme_from_repo():
    global latest_readme
    data = request.get_json()
    if not data or "repo_url" not in data:
        return jsonify({"error": "Missing repo_url in request data"}), 400

    repo_url = data.get("repo_url")
    
    try:
        # Fetch repository data using PyGithub
        repo_data = get_repo_data(repo_url)
        # Construct the prompt from repository data
        prompt = construct_prompt(repo_data)
        # Generate the README using the Gemini API
        generated_readme = generate_readme_with_gemini(prompt)
        if not generated_readme:
            return jsonify({"error": "No README generated"}), 500
        latest_readme = generated_readme
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"README": generated_readme})

@app.route('/download_readme', methods=["GET"])
def download_readme():
    global latest_readme
    if not latest_readme:
        return jsonify({"error": "No README generated yet"}), 400

    # Use BytesIO to create an in-memory file for download
    readme_bytes = BytesIO(latest_readme.encode('utf-8'))
    return send_file(readme_bytes, as_attachment=True, download_name="README.md", mimetype="text/markdown")

@app.route('/health', methods=["GET"])
def health():
    return jsonify({"message": "App is running and health endpoint is good"})

if __name__ == "__main__":
    app.run(debug=True)
