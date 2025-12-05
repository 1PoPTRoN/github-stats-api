<h1>🚀 GitHub Repository Explorer</h1>

A clean, fast, GitHub-themed web app that lets you analyze any public GitHub repository with real-time stats, visuals, CRUD history, and token-powered API access — built using FastAPI + Pydantic + httpx + Chart.js.

<h1>⭐ Features</h1>

🔍 Search any GitHub repo (owner/repo or URL)

👤 Displays owner avatar + repo details

📊 Chart.js visualization (Stars, Forks, Watchers, Issues)

🔐 GitHub Token Authentication (5,000 req/hr, no rate limits)

💾 JSON-based Data Persistence

🧩 Full CRUD

<ol>1. Create/Update → Auto-save repo stats</ol>

<ol>2. Read → History list</ol>

<ol>3. Delete → Remove repo from history</ol>

🎨 GitHub-style dark UI

⚡ Minimal, easy-to-understand codebase

🔥 Perfect for learning FastAPI + API integration + CRUD design

<h1>🏗️ Tech Stack</h1>
<table>
  <thead>
    <tr>
      <th>Layer</th>
      <th>Tech</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Backend</td>
      <td>FastAPI, Python</td>
    </tr>
    <tr>
      <td>API Client</td>
      <td>httpx</td>
    </tr>
    <tr>
      <td>Schema</td>
      <td>Pydantic</td>
    </tr>
    <tr>
      <td>Storage</td>
      <td>JSON file database</td>
    </tr>
    <tr>
      <td>Frontend</td>
      <td>HTML, CSS, JavaScript</td>
    </tr>
    <tr>
      <td>Charts</td>
      <td>Chart.js</td>
    </tr>
    <tr>
      <td>Auth</td>
      <td>GitHub Personal Access Token</td>
    </tr>
  </tbody>
</table>

<h1>🔧 Installation & Setup</h1>
<h3>1️⃣ Clone Repo</h3>
git clone https://github.com/1PoPTRoN/github-stats-api.git
cd repo-explorer

<h3>2️⃣ Install Dependencies</h3>
pip install fastapi uvicorn httpx pydantic

<h3>3️⃣ Set Your GitHub Token</h3>

<h5>Linux / macOS</h5>

export GITHUB_TOKEN="your_token_here"


<h5>Windows PowerShell</h5>

setx GITHUB_TOKEN "your_token_here"

<h3>4️⃣ Run Server</h3>
uvicorn main:app --reload

<h3>5️⃣ Open in Browser</h3>
http://localhost:8000

<h1>🧠 How It Works</h1>

<ol>1. User enters a GitHub repo → Frontend sends it to FastAPI</ol>

<ol>2. Backend fetches live data from GitHub API using token auth</ol>

<ol>3. Pydantic validates & structures data</ol>

<ol>4. JSON file stores repo (Create/Update)</ol>

<ol>5. User can view or delete saved repos (Read/Delete)</ol>

<ol>6. Chart.js visualizes repo stats</ol>

<h1>📚 API Routes</h1>
<ol>🔹 GET /api/repo-stats?repo=owner/repo</ol>

Fetch repo details + auto-save to history.

<ol>🔹 GET /api/history</ol>

Return all saved repositories.

<ol>🔹 DELETE /api/history?full_name=owner/repo</ol>

Delete a repository from saved history.

<h1>🗂️ Project Structure</h1>

root/<br>
├── main.py‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ # FastAPI backend<br>
├── index.html‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ # Frontend UI<br>
├── data/<br>
│   └── repositories.json‎ ‎ ‎ ‎ ‎ # Database (auto-created)<br>
└── README.md<br>

<h1>🚀 Future Enhancements</h1>

<ol>1. Repo comparison mode</ol>

<ol>2. Cloud deployment (Render/Railway/Vercel)</ol>

<ol>3. Switchable light/dark themes</ol>

<ol>4. Real database (SQLite/Postgres)</ol>

<ol>5. User login system</ol>

<h1>👨‍💻 Contributors</h1>

  Arpit – Backend + Frontend Integration

  Aabid Sattar – UI, CRUD, Documentation

<h1>⭐ If you like this project</h1>

Leave a star on GitHub! It motivates the devs 😎🌟
