import os
from github import Github

def get_repo_data(repo_url):
    # Try to get OAuth token from Flask-Dance if it's being used
    try:
        from flask_dance.contrib.github import github as flask_github
        token = flask_github.token.get("access_token") if flask_github.authorized else None
    except Exception:
        token = None

    # Fallback to .env token
    token = token or os.getenv("GITHUB_TOKEN")
    if not token:
        raise Exception("No GitHub token available. Please login or set GITHUB_TOKEN in your .env file.")

    # Parse owner/repo from URL
    parts = repo_url.rstrip("/").split("/")
    owner = parts[-2]
    repo_name = parts[-1]

    # Initialize GitHub client
    g = Github(token)
    repo = g.get_repo(f"{owner}/{repo_name}")

    # Get language info
    languages = repo.get_languages()  # {'JavaScript': 30000, 'Python': 15000, ...}
    primary_language = repo.language or (max(languages, key=languages.get) if languages else None)

    # Build metadata dictionary
    repo_data = {
        "name": repo.name,
        "full_name": repo.full_name,
        "description": repo.description,
        "owner": repo.owner.login,
        "language": primary_language,
        "languages_used": list(languages.keys()),
        "topics": repo.get_topics(),
        "license": repo.license.name if repo.license else None,
        "default_branch": repo.default_branch,
        "html_url": repo.html_url,
        "clone_url": repo.clone_url,
    }

    # Try to grab README
    try:
        readme = repo.get_readme()
        repo_data["readme"] = readme.decoded_content.decode("utf-8")
    except Exception:
        repo_data["readme"] = None

    # Grab dependency and build files if they exist
    project_files = [
        "requirements.txt", "package.json", "pyproject.toml",
        "go.mod", "Gemfile", "Pipfile", "composer.json"
    ]
    for filename in project_files:
        try:
            content = repo.get_contents(filename)
            repo_data[filename] = content.decoded_content.decode("utf-8")
        except Exception:
            repo_data[filename] = None


    return repo_data


def construct_prompt(repo_data, sections=None, styling=None):
    prompt = (
        "Create a comprehensive, detailed, and well-structured README for the following GitHub repository.\n"
        "Act as if README is offical and don't say things like the application's purpose and functionality are currently unspecified.\n"
        "The README should be written in Markdown format and include all relevant information.\n"
        "Do not include unnecessary placeholders (like 'Database Setup') unless there's evidence the project uses them.\n"
        "Ensure the output is easy to read, well-organized, and includes thorough explanations for each section.\n\n"
    )

    # Instruct to include a Built With section with technology badges.
    prompt += (
        "Additionally, include a 'Built With/Technologies' section. For each major technology used in the repository, "
        "display an inline badge (using Markdown image links from shields.io) that represents the technology. Also have this section be towards the top after the title of the repo"
        "Do not display the technology name as extra text—only the icon image should appear, as the icon itself includes the name. For example, output something like: Built With: ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoWidth=60) ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoWidth=60) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoWidth=60) Ensure that these badges appear inline with no additional text.\n\n"
    )
    
    prompt += f"Name: {repo_data.get('name')}\n"
    prompt += f"Description: {repo_data.get('description')}\n"
    prompt += f"Primary Language: {repo_data.get('language')}\n"

    if repo_data.get("languages_used"):
        prompt += f"Languages Used: {', '.join(repo_data['languages_used'])}\n"
    if repo_data.get("topics"):
        prompt += f"Topics: {', '.join(repo_data['topics'])}\n"

    topics = repo_data.get('topics') or []
    prompt += f"Topics: {', '.join(topics)}\n\n"

    owner = repo_data.get("owner")
    repo_name = repo_data.get("repo_name")
    clone_url = f"https://github.com/{owner}/{repo_name}.git"
    prompt += (
        "Include a clone command in a code block as follows:\n\n"
        "```bash\ngit clone " + clone_url + "\n```\n\n"
    )

    

    # Add dependency data
    if repo_data.get("requirements.txt"):
        prompt += f"Dependencies (Python - requirements.txt):\n{repo_data['requirements.txt']}\n\n"
    if repo_data.get("package.json"):
        prompt += f"Dependencies (Node - package.json):\n{repo_data['package.json']}\n\n"
    if repo_data.get("pyproject.toml"):
        prompt += f"Dependencies (Python - pyproject.toml):\n{repo_data['pyproject.toml']}\n\n"
    if repo_data.get("go.mod"):
        prompt += f"Dependencies (Go - go.mod):\n{repo_data['go.mod']}\n\n"
    if repo_data.get("composer.json"):
        prompt += f"Dependencies (PHP - composer.json):\n{repo_data['composer.json']}\n\n"

    # Process custom section settings.
    if sections:
        selected_sections = [key for key, include in sections.items() if include]
        omitted_sections = [key for key, include in sections.items() if not include]
        
        if selected_sections:
            prompt += "The README should include detailed information for the following sections:\n"
            for sec in selected_sections:
                prompt += f"- {sec}\n"
            prompt += "\n"
        
        if omitted_sections:
            prompt += (
                "Do not include separate headings for the following sections: " 
                + ", ".join(omitted_sections) 
                + ". However, ensure that all vital repository details are still covered.\n\n"
            )
    else:
        prompt += (
            "Include standard sections such as Overview, Installation, Usage, Contributing, and License, "
            "ensuring each section is thorough and detailed.\n\n"
        )

    # Process custom styling settings.
    if styling:
        prompt += "Apply the following styling options to the formatting of the README:\n"
        for key, value in styling.items():
            prompt += f"- {key}: {value}\n"
        prompt += "\n"
    
    # Final instruction reinforcing detail and clarity.
    prompt += (
        "Ensure the final README is comprehensive, detailed, and well-organized, with a clear structure and "
        "thorough explanations. Do not enclose the entire output in code fences. Never have a Project Structure section because AI is usually off about those."
    )

    print(prompt)
    return prompt
