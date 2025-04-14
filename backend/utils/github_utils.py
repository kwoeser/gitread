import os
from github import Github

def get_repo_data(repo_url):
    # Try to get OAuth token from Flask-Dance (if configured)
    try:
        from flask_dance.contrib.github import github as flask_github
        token = flask_github.token.get("access_token") if flask_github.authorized else None
    except Exception:
        token = None

    # Fallback to environment token if OAuth token is not available
    if not token:
        token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise Exception("No GitHub token available. Please login with GitHub or set GITHUB_TOKEN in your .env.")

    g = Github(token)
    parts = repo_url.rstrip('/').split('/')
    owner = parts[-2]
    repo_name = parts[-1]
    repo = g.get_repo(f"{owner}/{repo_name}")
    
    repo_data = {
        "name": repo.name,
        "description": repo.description,
        "language": repo.language,
        "topics": repo.get_topics(),
        "owner": owner,
        "repo_name": repo_name,
    }
    
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

def construct_prompt(repo_data, sections=None, styling=None):
    # Begin with a clear, comprehensive instruction.
    prompt = (
        "Generate a comprehensive, detailed, and well-structured README for the following GitHub repository. "
        "The README should be written in Markdown format and include all relevant information. "
        "Ensure the output is easy to read, well-organized, and includes thorough explanations for each section.\n\n"
    )
    
    # Include basic repository details.
    prompt += f"Name: {repo_data.get('name')}\n"
    prompt += f"Description: {repo_data.get('description')}\n"
    prompt += f"Primary Language: {repo_data.get('language')}\n"
    topics = repo_data.get('topics') or []
    prompt += f"Topics: {', '.join(topics)}\n\n"
    
    owner = repo_data.get("owner")
    repo_name = repo_data.get("repo_name")
    clone_url = f"https://github.com/{owner}/{repo_name}.git"
    prompt += (
        "Include a clone command in a code block as follows:\n\n"
        "```bash\ngit clone " + clone_url + "\n```\n\n"
    )
    
    # Add dependency information.
    if repo_data.get("requirements"):
        prompt += f"Dependencies (from requirements.txt):\n{repo_data.get('requirements')}\n\n"
    if repo_data.get("package_json"):
        prompt += f"Dependencies (from package.json):\n{repo_data.get('package_json')}\n\n"
    
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
    
    # Instruct to include a Built With section with technology badges.
    prompt += (
        "Additionally, include a 'Built With' section. For each major technology used in the repository, "
        "display an inline badge (using Markdown image links from shields.io) that represents the technology. "
        "Only the badge image should appear (with no extra text).\n\n"
    )
    
    # Final instruction reinforcing detail and clarity.
    prompt += (
        "Ensure the final README is comprehensive, detailed, and well-organized, with a clear structure and "
        "thorough explanations. Do not enclose the entire output in code fences."
    )
    
    print(prompt)  # Useful for debugging and seeing the generated prompt.
    return prompt


