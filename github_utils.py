# github_utils.py
from github import Github
import os

def get_repo_data(repo_url):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise Exception("Missing GitHub token. Please set GITHUB_TOKEN in your .env file.")
    
    g = Github(token)
    # Example URL: "https://github.com/owner/repo"
    parts = repo_url.rstrip('/').split('/')
    owner = parts[-2]
    repo_name = parts[-1]
    repo = g.get_repo(f"{owner}/{repo_name}")
    
    repo_data = {
        "name": repo.name,
        "description": repo.description,
        "language": repo.language,
        "topics": repo.get_topics(),
    }
    
    # Try to fetch key files if they exist.
    try:
        requirements_file = repo.get_contents("requirements.txt")
        repo_data["requirements"] = requirements_file.decoded_content.decode('utf-8')
    except Exception:
        repo_data["requirements"] = None

    try:
        package_file = repo.get_contents("package.json")
        repo_data["package_json"] = package_file.decoded_content.decode('utf-8')
    except Exception:
        repo_data["package_json"] = None

    return repo_data

def construct_prompt(repo_data):
    prompt = "Generate a comprehensive README for a GitHub repository with the following details:\n\n"
    prompt += f"Name: {repo_data.get('name')}\n"
    prompt += f"Description: {repo_data.get('description')}\n"
    prompt += f"Primary Language: {repo_data.get('language')}\n"
    topics = repo_data.get('topics') or []
    prompt += f"Topics: {', '.join(topics)}\n\n"
    
    if repo_data.get("requirements"):
        prompt += f"Dependencies (from requirements.txt):\n{repo_data.get('requirements')}\n\n"
    if repo_data.get("package_json"):
        prompt += f"Dependencies (from package.json):\n{repo_data.get('package_json')}\n\n"
    
    prompt += (
        "Please generate a README in Markdown format including sections such as "
        "Overview, Installation, Usage, Contributing, and License."
    )
    return prompt
