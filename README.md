# GitHub Sizing

GitHub Sizing is a small Flask + vanilla JS app that returns the stats and size of a GitHub repository. Enter a repo in `owner/repo` format (or a GitHub URL) and it shows key metrics plus optional raw JSON.

## What it returns
- Repo name and owner
- Size in KB (from the GitHub API)
- Collaborator list and count (token required for private repos)
- Commit count

## Quick start
1. python -m venv .venv
2. Activate the venv:
   - macOS/Linux: source .venv/bin/activate
   - Windows: .venv\Scripts\activate
3. pip install -r requirements.txt
4. python src/main/app.py
5. Open http://localhost:5000

## Usage
- Enter `owner/repo` or `https://github.com/owner/repo`
- Optional: set `GITHUB_TOKEN` or paste a token in the UI to fetch collaborator data.

## API (optional)
POST `/api/github-data`
- body: `{"repo":"owner/repo","include_raw":false,"token":"...optional"}`

POST `/api/commit-count`
- body: `{"repo":"owner/repo","token":"...optional"}`
