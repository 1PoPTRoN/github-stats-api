from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
import os


app = FastAPI()

GITHUB_TOKEN = os.getenv("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")


# -----------------------------
# Home route: serves index.html
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="index.html file not found")

    return HTMLResponse(html)

def parse_repo(raw: str) -> tuple[str, str]:
    text = raw.strip()

    if "github.com" in text:
        text = text.split("github.com/", 1)[1]

    parts = text.strip("/").split("/")

    if len(parts) < 2:
        raise HTTPException(
            status_code=400,
            detail="Enter repository as 'owner/repo' or full GitHub URL.",
        )

    owner = parts[0]
    repo = parts[1]
    return owner, repo

@app.get("/api/repo-stats")
def repo_stats(repo: str):
    owner, name = parse_repo(repo)
    url = f"https://api.github.com/repos/{owner}/{name}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-repo-explorer",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    try:
        response = httpx.get(url, headers=headers, timeout=10)
    except httpx.RequestError as exc:
        print("Error contacting GitHub:", exc)
        raise HTTPException(status_code=502, detail="Could not reach GitHub API.")

    # handle common error cases
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Repository not found.")

    if response.status_code == 403:
        # usually rate limit / permission
        msg = response.json().get("message", "Forbidden / rate limited by GitHub.")
        print("GitHub 403:", msg)
        raise HTTPException(status_code=502, detail=msg)

    if response.status_code != 200:
        print("GitHub error:", response.status_code, response.text)
        raise HTTPException(
            status_code=502,
            detail=f"GitHub error: {response.status_code}",
        )

    data = response.json()

    result = {
        "full_name": data.get("full_name"),
        "html_url": data.get("html_url"),
        "description": data.get("description"),
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "watchers": data.get("watchers_count"),
        "open_issues": data.get("open_issues_count"),
        "pushed_at": data.get("pushed_at"),
        "updated_at": data.get("updated_at"),
        "owner": {
            "login": data.get("owner", {}).get("login"),
            "avatar_url": data.get("owner", {}).get("avatar_url"),
        },
    }


    return JSONResponse(result)

