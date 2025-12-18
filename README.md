# GitHub Repository Explorer

A clean, fast, GitHub-themed web app that lets you analyze any public GitHub repository with real-time stats, visuals, CRUD history, and token-powered API access — built using **FastAPI**, **Pydantic**, **httpx**, and **Chart.js**.

## Features

- Search any GitHub repository (`owner/repo` or full URL)
- Displays owner avatar + repo details
- Chart.js visualizations (Stars, Forks, Watchers, Issues)
- GitHub Token Authentication (up to 5,000 requests/hr)
- JSON-based Data Persistence
- Full CRUD functionality:
  - **Create/Update** → Auto-save repo stats  
  - **Read** → View history list  
  - **Delete** → Remove from history  
- GitHub-style Dark UI  
- Minimal, beginner-friendly codebase  
- Perfect for learning FastAPI + API integration + CRUD logic  

## Tech Stack

| Layer      | Tech                          |
|------------|-------------------------------|
| Backend    | FastAPI, Python               |
| API Client | httpx                         |
| Schema     | Pydantic                      |
| Storage    | JSON File Database            |
| Frontend   | HTML, CSS, JavaScript         |
| Charts     | Chart.js                      |
| Auth       | GitHub Personal Access Token  |

## Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/1PoPTRoN/github-stats-api.git
cd github-stats-api
```

### **2️⃣ Setting up virtual environment**
  #### **Linux / macOS**
  ```bash
  python3 -m venv <folder-name>
  source <folder-name>/bin/activate
  ```

  #### **Windows**
  ```bash
  python -m venv <folder-name>
  <folder-name>/Scripts/activate
  ```

### **3️⃣ Install Dependencies**
```bash
pip install fastapi uvicorn httpx pydantic
```

### **4️⃣ Set Your GitHub Token**
  #### **Linux / macOS**
  ```bash
  export GITHUB_TOKEN="your_token_here"
  ```

  #### **Windows PowerShell**
  ```bash
  setx GITHUB_TOKEN "your_token_here"
  ```

### **5️⃣ Run the FastAPI Server**
```bash
uvicorn main:app --reload
```

### **6️⃣ Open the Web App**
```bash
http://localhost:8000
```

## How It Works

- User enters a repository → frontend sends it to FastAPI
- Backend fetches live GitHub data using httpx
- Pydantic validates & structures the API response
- Repository stats are stored or updated in the JSON database
- User can view or delete items from history
- Chart.js generates dynamic repo stat visualizations



## API Routes

- GET /api/repo-stats?repo=owner/repo
  - Fetch repo stats & auto-save to history.
- GET /api/history
  - Returns all saved repositories.
- DELETE /api/history?full_name=owner/repo
  - Deletes the specified repo from the history database.

## Project Structure

```bash
root/
├── main.py                # FastAPI backend
├── index.html             # Frontend UI
├── data/
│   └── repositories.json  # Auto-created JSON database
└── README.md
```

## Future Enhancements

- Repo comparison mode
- Cloud deployment (Render / Railway / Vercel)
- Light / Dark mode switch
- SQLite / Postgres database support
- User login + profiles

## 👨‍💻 Contributors

- Arpit – Backend + Frontend Integration
- Aabid Sattar – UI, CRUD, Documentation

## ⭐ Support the Project

If this project helped you or you learned something cool, drop a ⭐ on GitHub — it keeps the devs motivated 😎🔥
