from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
import os

app = FastAPI()

GITHUB_TOKEN = os.getenv("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")


@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="index.html not found")


def parse_repo(raw: str):
    raw = raw.strip()

    if "github.com" in raw:
        raw = raw.split("github.com/", 1)[1]

    parts = raw.strip("/").split("/")
    if len(parts) < 2:
        raise HTTPException(
            status_code=400,
            detail="Enter repo as owner/repo or full GitHub URL.",
        )

    return parts[0], parts[1]


@app.get("/api/repo-stats")
def repo_stats(repo: str):
    owner, name = parse_repo(repo)
    url = f"https://api.github.com/repos/{owner}/{name}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-explorer-demo",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    else:
        print("!! WARNING: No GITHUB_TOKEN found in environment")

    try:
        resp = httpx.get(url, headers=headers, timeout=10)
    except httpx.RequestError as exc:
        print("Error contacting GitHub:", exc)
        raise HTTPException(status_code=502, detail="Could not reach GitHub API")

    print("GitHub status:", resp.status_code)

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Repository not found")

    if resp.status_code == 403:
        body = resp.json()
        msg = body.get("message", "Forbidden / rate limited")
        print("GitHub 403:", msg)
        raise HTTPException(status_code=502, detail=msg)

    if resp.status_code != 200:
        print("GitHub error:", resp.status_code, resp.text)
        raise HTTPException(status_code=502, detail=f"GitHub error {resp.status_code}")

    data = resp.json()

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
