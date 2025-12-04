from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import httpx
import os
import json

app = FastAPI()

# -------------------------
# GitHub Token (from env)
# -------------------------
GITHUB_TOKEN = os.getenv("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")  # set this in your shell

print("DEBUG: GITHUB_TOKEN loaded?", bool(GITHUB_TOKEN))  # will print True/False


# -------------------------
# Serve frontend
# -------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("index.html", "r", encoding="utf-8") as file:
            return HTMLResponse(file.read())
    except Exception:
        raise HTTPException(status_code=500, detail="index.html missing")


# -------------------------
# Helper: parse repo input
# -------------------------
def parse_repo(raw: str):
    raw = raw.strip()
    if "github.com" in raw:
        raw = raw.split("github.com/", 1)[1]

    parts = raw.strip("/").split("/")
    if len(parts) < 2:
        raise HTTPException(
            status_code=400,
            detail="Enter repo in format: owner/repo or full GitHub URL",
        )
    return parts[0], parts[1]


# -------------------------
# Pydantic "DB schema"
# -------------------------
class RepoModel(BaseModel):
    full_name: str | None
    html_url: str | None
    description: str | None
    stars: int | None
    forks: int | None
    watchers: int | None
    open_issues: int | None
    pushed_at: str | None
    updated_at: str | None
    owner_login: str | None
    owner_avatar: str | None


DATA_PATH = "data/repositories.json"


# -------------------------
# Load / Save helpers
# -------------------------
def load_all_repos():
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_repo_to_file(repo: RepoModel):
    os.makedirs("data", exist_ok=True)
    existing = load_all_repos()

    updated = False
    for i, item in enumerate(existing):
        if item.get("full_name") == repo.full_name:
            existing[i] = repo.dict()
            updated = True
            break

    if not updated:
        existing.append(repo.dict())

    with open(DATA_PATH, "w") as f:
        json.dump(existing, f, indent=4)


# -------------------------
# Main API: fetch repo stats
# -------------------------
@app.get("/api/repo-stats")
def repo_stats(repo: str):
    owner, name = parse_repo(repo)
    url = f"https://api.github.com/repos/{owner}/{name}"

    # Build headers
    headers = {
        "User-Agent": "github-repo-explorer",
        "Accept": "application/vnd.github+json",
    }
    if GITHUB_TOKEN:
        # classic token format
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        response = httpx.get(url, headers=headers, timeout=10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub unreachable: {e}")

    # Log for debugging
    print("DEBUG: GitHub status:", response.status_code)
    if response.status_code != 200:
        print("DEBUG: GitHub response text:", response.text)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Repository not found")

    if response.status_code == 401 or response.status_code == 403:
        raise HTTPException(
            status_code=500,
            detail="GitHub auth error. Check your token (wrong / missing / insufficient scopes).",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"GitHub API error: {response.status_code}",
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

    repo_obj = RepoModel(
        full_name=result["full_name"],
        html_url=result["html_url"],
        description=result["description"],
        stars=result["stars"],
        forks=result["forks"],
        watchers=result["watchers"],
        open_issues=result["open_issues"],
        pushed_at=result["pushed_at"],
        updated_at=result["updated_at"],
        owner_login=result["owner"]["login"],
        owner_avatar=result["owner"]["avatar_url"],
    )

    save_repo_to_file(repo_obj)
    return JSONResponse(result)


# -------------------------
# READ history
# -------------------------
@app.get("/api/history")
def get_history():
    return JSONResponse(load_all_repos())


# -------------------------
# DELETE from history
# -------------------------
@app.delete("/api/history")
def delete_repo(full_name: str):
    existing = load_all_repos()
    new_data = [i for i in existing if i.get("full_name") != full_name]

    if len(new_data) == len(existing):
        raise HTTPException(status_code=404, detail="Repository not found")

    with open(DATA_PATH, "w") as f:
        json.dump(new_data, f, indent=4)

    return {"detail": f"{full_name} deleted"}