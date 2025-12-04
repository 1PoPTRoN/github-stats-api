from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import httpx

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("index.html", "r", encoding="utf-8") as file:
            return HTMLResponse(file.read())
    except:
        raise HTTPException(status_code=500, detail="index.html missing")

def parse_repo(raw):
    raw = raw.strip()

    if "github.com" in raw:
        raw = raw.split("github.com/", 1)[1]

    parts = raw.strip("/").split("/")
    if len(parts) < 2:
        raise HTTPException(
            status_code=400,
            detail="Enter repo in format: owner/repo or GitHub URL",
        )

    return parts[0], parts[1]

@app.get("/api/repo-stats")
def repo_stats(repo: str):
    owner, name = parse_repo(repo)
    github_api = f"https://api.github.com/repos/{owner}/{name}"

    try:
        response = httpx.get(
            github_api,
            headers={"User-Agent": "fastapi-repo-explorer"},
            timeout=10
        )
    except:
        raise HTTPException(status_code=500, detail="Could not reach GitHub")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Repository not found")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="GitHub API error")

    repo_data = response.json()

    result = {
        "full_name": repo_data.get("full_name"),
        "html_url": repo_data.get("html_url"),
        "description": repo_data.get("description"),
        "stars": repo_data.get("stargazers_count"),
        "forks": repo_data.get("forks_count"),
        "watchers": repo_data.get("watchers_count"),
        "open_issues": repo_data.get("open_issues_count"),
        "pushed_at": repo_data.get("pushed_at"),
        "updated_at": repo_data.get("updated_at"),
        "owner": {
            "login": repo_data.get("owner", {}).get("login"),
            "avatar_url": repo_data.get("owner", {}).get("avatar_url"),
            },
    }

    return JSONResponse(result)