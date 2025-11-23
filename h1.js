const btn = document.getElementById("checkBtn");
const repoUrlInput = document.getElementById("repoUrl");
const errorDiv = document.getElementById("error");
const repoInfo = document.getElementById("repoInfo");
const statusBadge = document.getElementById("statusBadge");
const avatarImg = document.getElementById("avatar");
const repoDescEl = document.getElementById("repoDesc");
const redirectBtn = document.getElementById("redirectBtn");
const repoNameText = document.getElementById("repoName");
const lastUpdatedText = document.getElementById("lastUpdated");

let barChartInstance = null;

// small helpers
const setText = (id, value) => {
    document.getElementById(id).textContent = value;
};

function parseGitHubUrl(raw) {
    try {
        const url = new URL(raw.trim());
        if (url.hostname !== "github.com") 
            return null;

        const [owner, repo] = url.pathname.replace(/^\/+/, "").split("/");
        if (!owner || !repo)
            return null;

        return { owner, repo };
    } catch {
        return null;
        }
    }

function getHealthStatus(pushedAt) {
    const last = new Date(pushedAt);
    const days = (Date.now() - last.getTime()) / (1000 * 60 * 60 * 24);

    if (days <= 30) return { label: "Very Active", className: "status-active" };
    if (days <= 180) return { label: "Maintained", className: "status-active" };
    if (days <= 365) return { label: "Stale", className: "status-stale" };
    return { label: "Dead", className: "status-dead" };
}

async function fetchRepoData() {
    errorDiv.textContent = "";
    repoInfo.style.display = "none";

    const parsed = parseGitHubUrl(repoUrlInput.value);
    if (!parsed) {
        errorDiv.textContent = "Invalid GitHub repo URL.";
        return;
    }

    const { owner, repo } = parsed;
    const url = `https://api.github.com/repos/${owner}/${repo}`;

    btn.disabled = true;
    btn.textContent = "Analyzing…";

    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error("GitHub API error");

        const data = await res.json();

        const {
            full_name,
            description,
            html_url,
            stargazers_count = 0,
            forks_count = 0,
            subscribers_count,
            watchers_count,
            open_issues_count = 0,
            pushed_at,
            updated_at,
            owner: ownerObj,
        } = data;

        const watchers = subscribers_count ?? watchers_count ?? 0;

        // top section
        repoNameText.textContent = full_name;
        repoDescEl.textContent = description || "No description provided.";
        avatarImg.src = ownerObj?.avatar_url || "";
        redirectBtn.href = html_url;
        lastUpdatedText.textContent = `Last push: ${new Date(pushed_at).toLocaleString()} • ` + `Updated: ${new Date(updated_at).toLocaleString()}`;

        // stats
        setText("stars", stargazers_count);
        setText("forks", forks_count);
        setText("watchers", watchers);
        setText("issues", open_issues_count);

        // health badge
        const health = getHealthStatus(pushed_at);
        statusBadge.textContent = health.label;
        statusBadge.className = `status-badge ${health.className}`;

        // show card
        repoInfo.style.display = "block";

        // chart
        const ctx = document.getElementById("barChart").getContext("2d");
        if (barChartInstance) barChartInstance.destroy();

        barChartInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Stars", "Forks", "Watchers", "Open issues"],
                datasets: [
                {
            label: "Repo stats",
            data: [stargazers_count, forks_count, watchers, open_issues_count],
          },
        ],
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true } },
      },
    });
  } catch (err) {
    console.error(err);
    errorDiv.textContent = "Could not fetch repo. Check URL or API rate limit.";
  } finally {
    btn.disabled = false;
    btn.textContent = "Analyze ↵";
  }
}

btn.addEventListener("click", fetchRepoData);
repoUrlInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") fetchRepoData();
});