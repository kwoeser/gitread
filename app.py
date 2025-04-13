# app.py
import os
from flask import Flask, request, jsonify, send_file, make_response
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

# needed helper function to remove markdown at start of file
# def clean_readme(text):
#     # Remove a leading code fence if it exists
#     if text.startswith("```markdown"):
#         text = text[len("```markdown"):].lstrip()
#     elif text.startswith("```"):
#         text = text[len("```"):].lstrip()
    
#     # Remove trailing code fence if it exists
#     if text.endswith("```"):
#         text = text[:-3].rstrip()
#     return text

def clean_readme(text):
    # Split the text into lines
    lines = text.splitlines()
    
    # Remove the first line if it starts with a code fence (e.g., ``` or ```markdown)
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    
    # Remove the last line if it starts with a code fence
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    
    # Re-join the lines back into a string
    return "\n".join(lines)



@app.route('/generate_readme_from_repo', methods=["POST"])
def generate_readme_from_repo():
    global latest_readme
    data = request.get_json()
    if not data or "repo_url" not in data:
        return jsonify({"error": "Missing repo_url in request data"}), 400

    repo_url = data.get("repo_url")
    
    try:
        repo_data = get_repo_data(repo_url)
        prompt = construct_prompt(repo_data)
        generated_readme = generate_readme_with_gemini(prompt)
        generated_readme = clean_readme(generated_readme)
        if not generated_readme:
            return jsonify({"error": "No README generated"}), 500

        latest_readme = generated_readme
        print("Generated README updated in global variable:")
        print(latest_readme)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"README": generated_readme})




@app.route('/download_readme', methods=["GET"])
def download_readme():
    global latest_readme
    if not latest_readme:
        return jsonify({"error": "No README generated yet"}), 400

    # Encode the README content
    readme_content = latest_readme.encode('utf-8')
    
    # Build the response using make_response
    response = make_response(readme_content)
    
    # Set headers to force download with the correct filename and extension
    response.headers['Content-Disposition'] = 'attachment; filename="README.md"'
    response.headers['Content-Type'] = 'text/markdown'
    
    return response


@app.route('/health', methods=["GET"])
def health():
    return jsonify({"message": "App is running and health endpoint is good"})

if __name__ == "__main__":
    app.run(debug=True)
