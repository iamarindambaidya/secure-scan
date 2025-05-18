import requests
import os

GITHUB_API_URL = "https://api.github.com"

def create_github_issue(repo, title, body):
    token = 'your real token'  # export your real token

    if not token:
        print("⚠️ GitHub token not set in environment variable `GITHUB_TOKEN`")
        return

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "title": title,
        "body": body,
        "labels": ["security-scan"]
    }

    response = requests.post(
        f"{GITHUB_API_URL}/repos/{repo}/issues",
        headers=headers,
        json=data
    )

    if response.status_code == 201:
        print(f"✅ Issue created: {response.json()['html_url']}")
    else:
        print(f"❌ Failed to create issue: {response.status_code} {response.text}")
