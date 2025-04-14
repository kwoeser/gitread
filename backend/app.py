import os
from flask import Flask, request, jsonify, send_file, make_response, redirect, url_for, session
from flask_cors import CORS
from dotenv import load_dotenv
from io import BytesIO
from flask_session import Session  # Import Flask-Session

# Import utilities from the utils package
from utils.github_utils import get_repo_data, construct_prompt
from utils.ai_utils import generate_readme_with_gemini

# Load environment variables
load_dotenv()

# Ensure OAuth works over HTTP in development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersekrit")
CORS(app)

# Configure Flask-Session to use filesystem-based sessions with an absolute path
session_dir = os.path.abspath("./.flask_session/")
if not os.path.exists(session_dir):
    os.makedirs(session_dir)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = session_dir
app.config["SESSION_COOKIE_SECURE"] = False  # Not using HTTPS in development
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_PATH"] = '/'
app.config["SESSION_PERMANENT"] = False
Session(app)

# Log session contents for debugging
@app.before_request
def log_session():
    print("Session contents:", dict(session))

@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response

# Register GitHub OAuth blueprint using Flask-Dance
from flask_dance.contrib.github import make_github_blueprint, github
github_bp = make_github_blueprint(
    client_id=os.getenv("GITHUB_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_OAUTH_CLIENT_SECRET"),
    scope="repo",
    redirect_to="post_auth"  # Ensures callback goes to /post_auth
)
app.register_blueprint(github_bp, url_prefix="/github_login")

# Global variable for demo purposes
latest_readme = None

def clean_readme(text):
    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)

@app.route('/')
def home():
    return "Welcome to the GitHub README Generator Home Page!"

# Endpoint to generate README from a repo URL.
@app.route('/generate_readme_from_repo', methods=["POST"])
def generate_readme_from_repo():
    global latest_readme
    data = request.get_json()
    if not data or "repo_url" not in data:
        return jsonify({"error": "Missing repo_url in request data"}), 400

    repo_url = data.get("repo_url")
    # Extract custom settings (if provided)
    custom_sections = data.get("sections", {})
    custom_styling = data.get("styling", {})

    try:
        repo_data = get_repo_data(repo_url)
        # Pass custom settings to the prompt constructor
        prompt = construct_prompt(repo_data, custom_sections, custom_styling)
        generated_readme = generate_readme_with_gemini(prompt)
        generated_readme = clean_readme(generated_readme)
        if not generated_readme:
            return jsonify({"error": "No README generated"}), 500

        latest_readme = generated_readme
        print("Generated README updated:")
        print(latest_readme)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"README": generated_readme})

# Endpoint to download the generated README.
@app.route('/download_readme', methods=["GET"])
def download_readme():
    global latest_readme
    if not latest_readme:
        return jsonify({"error": "No README generated yet"}), 400

    readme_content = latest_readme.encode('utf-8')
    response = make_response(readme_content)
    response.headers['Content-Disposition'] = 'attachment; filename="README.md"'
    response.headers['Content-Type'] = 'text/markdown'
    return response

@app.route('/health', methods=["GET"])
def health():
    return jsonify({"message": "App is running and health endpoint is good"})

# Endpoint to return auth status.
@app.route('/auth/status')
def auth_status():
    if 'github_oauth_token' in session:
        return jsonify({"connected": True})
    return jsonify({"connected": False})

# Endpoint to fetch repositories using the OAuth token.
@app.route('/repos')
def repos():
    if 'github_oauth_token' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    token = session['github_oauth_token'].get('access_token')
    if not token:
        return jsonify({"error": "No access token found in session"}), 401

    try:
        from github import Github
        g = Github(token)
        user = g.get_user()
        repos = user.get_repos()
        repos_data = [
            {"id": repo.id, "full_name": repo.full_name, "html_url": repo.html_url}
            for repo in repos
        ]
        return jsonify(repos_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GitHub OAuth login route
@app.route('/login/github')
def login_github():
    return redirect(url_for("github.login"))

# Logout endpoint clears the session and cookie
@app.route('/logout')
def logout():
    session.clear()
    response = redirect("http://localhost:5173")  # Redirect to your frontend login page
    response.set_cookie(app.config.get("SESSION_COOKIE_NAME", "session"), '', expires=0)
    return response

@app.route('/post_auth')
def post_auth():
    if github.authorized:
        resp = github.get("/user")
        if resp.ok:
            user_info = resp.json()
            print("Logged in as:", user_info["login"])
        # Redirect to your frontend running on port 5173
        return redirect("http://localhost:5173")
    else:
        return redirect(url_for("login_github"))

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
