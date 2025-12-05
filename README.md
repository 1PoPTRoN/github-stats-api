<h1>🚀 GitHub Repository Explorer</h1>

A clean, fast, GitHub-themed web app that lets you analyze any public GitHub repository with real-time stats, visuals, CRUD history, and token-powered API access — built using FastAPI + Pydantic + httpx + Chart.js.

⭐ Features

🔍 Search any GitHub repo (owner/repo or URL)

👤 Displays owner avatar + repo details

📊 Chart.js visualization (Stars, Forks, Watchers, Issues)

🔐 GitHub Token Authentication (5,000 req/hr, no rate limits)

💾 JSON-based Data Persistence

🧩 Full CRUD

Create/Update → Auto-save repo stats

Read → History list

Delete → Remove repo from history

🎨 GitHub-style dark UI

⚡ Minimal, easy-to-understand codebase

🔥 Perfect for learning FastAPI + API integration + CRUD design

🏗️ Tech Stack
Layer	Tech
Backend	FastAPI, Python
API Client	httpx
Schema	Pydantic
Storage	JSON file database
Frontend	HTML, CSS, JavaScript
Charts	Chart.js
Auth	GitHub Personal Access Token
📸 Screenshots (Add yours)
📁 /screenshots
    ui.png
    chart.png
    history.png


Add images here once you run the project.

🔧 Installation & Setup
1️⃣ Clone Repo
git clone https://github.com/your-username/repo-explorer.git
cd repo-explorer

2️⃣ Install Dependencies
pip install fastapi uvicorn httpx pydantic

3️⃣ Set Your GitHub Token

Linux / macOS

export GITHUB_TOKEN="your_token_here"


Windows PowerShell

setx GITHUB_TOKEN "your_token_here"

4️⃣ Run Server
uvicorn main:app --reload

5️⃣ Open in Browser
http://localhost:8000

🧠 How It Works

User enters a GitHub repo → Frontend sends it to FastAPI

Backend fetches live data from GitHub API using token auth

Pydantic validates & structures data

JSON file stores repo (Create/Update)

User can view or delete saved repos (Read/Delete)

Chart.js visualizes repo stats

📚 API Routes
🔹 GET /api/repo-stats?repo=owner/repo

Fetch repo details + auto-save to history.

🔹 GET /api/history

Return all saved repositories.

🔹 DELETE /api/history?full_name=owner/repo

Delete a repository from saved history.

🗂️ Project Structure
root/
├── main.py              # FastAPI backend
├── index.html           # Frontend UI
├── data/
│   └── repositories.json # Database (auto-created)
└── README.md

🚀 Future Enhancements

Repo comparison mode

Cloud deployment (Render/Railway/Vercel)

Switchable light/dark themes

Real database (SQLite/Postgres)

User login system

👨‍💻 Contributors

Arpit – Backend + Frontend Integration

Teammate – UI, CRUD, Documentation

⭐ If you like this project

Leave a star on GitHub! It motivates the devs 😎🌟
