import os
import re

import requests
from flask import Flask, jsonify, request, send_from_directory


FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
)

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")


def parse_repo_identifier(value):
    if not value:
        return None
    raw = value.strip()
    if not raw:
        return None

    patterns = [
        r"^https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)",
        r"^git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/]+)",
    ]
    for pattern in patterns:
        match = re.match(pattern, raw, re.IGNORECASE)
        if match:
            owner = match.group("owner")
            repo = match.group("repo")
            break
    else:
        if "/" not in raw:
            return None
        owner, repo = raw.split("/", 1)

    owner = owner.strip()
    repo = repo.strip().strip("/")
    if repo.endswith(".git"):
        repo = repo[:-4]
    if "/" in repo:
        repo = repo.split("/", 1)[0]

    if not owner or not repo:
        return None
    return owner, repo


def build_headers(token):
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def safe_json(response):
    try:
        return response.json()
    except ValueError:
        return None


def extract_last_page(link_header):
    if not link_header:
        return None
    for part in link_header.split(","):
        section = part.strip().split(";")
        if len(section) < 2:
            continue
        url_part = section[0].strip()
        rel_part = None
        for segment in section[1:]:
            segment = segment.strip()
            if segment.startswith("rel="):
                rel_part = segment[4:].strip('"')
                break
        if rel_part == "last" and url_part.startswith("<") and url_part.endswith(">"):
            match = re.search(r"[?&]page=(\d+)", url_part)
            if match:
                return int(match.group(1))
    return None


def fetch_commit_count(owner, repo, headers):
    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(
        commits_url, headers=headers, params={"per_page": 1}, timeout=15
    )
    if response.status_code == 409:
        return 0, response
    if response.status_code != 200:
        return None, response
    last_page = extract_last_page(response.headers.get("Link"))
    if last_page is not None:
        return last_page, response
    commits = safe_json(response) or []
    return len(commits), response


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/api/github-data", methods=["POST"])
def github_data():
    payload = request.get_json(silent=True) or {}
    repo_input = (payload.get("repo") or "").strip()
    include_raw = bool(payload.get("include_raw"))
    token = (payload.get("token") or os.getenv("GITHUB_TOKEN") or "").strip()

    parsed = parse_repo_identifier(repo_input)
    if not parsed:
        return (
            jsonify({"error": "Invalid repo format. Use owner/repo or a GitHub URL."}),
            400,
        )

    owner, repo = parsed
    headers = build_headers(token)

    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    repo_response = requests.get(repo_url, headers=headers, timeout=15)
    if repo_response.status_code != 200:
        message = None
        repo_body = safe_json(repo_response)
        if isinstance(repo_body, dict):
            message = repo_body.get("message")
        return (
            jsonify(
                {
                    "error": "GitHub repo request failed.",
                    "status_code": repo_response.status_code,
                    "message": message or repo_response.text.strip(),
                }
            ),
            repo_response.status_code,
        )

    repo_data = repo_response.json()

    collab_url = f"https://api.github.com/repos/{owner}/{repo}/collaborators"
    collab_response = requests.get(
        collab_url, headers=headers, params={"per_page": 100}, timeout=15
    )

    collaborators = []
    collab_warning = None
    if collab_response.status_code == 200:
        collab_data = collab_response.json()
        for collaborator in collab_data:
            collaborators.append(
                {"username": collaborator.get("login"), "id": collaborator.get("id")}
            )
    else:
        collab_body = safe_json(collab_response)
        collab_warning = {
            "message": "Collaborators request failed.",
            "status_code": collab_response.status_code,
            "details": (
                collab_body.get("message")
                if isinstance(collab_body, dict)
                else collab_response.text.strip()
            ),
        }

    filtered = {
        "repoName": repo_data.get("name"),
        "owner": (repo_data.get("owner") or {}).get("login"),
        "size": repo_data.get("size"),
        "collaborators": collaborators,
    }

    response_payload = {"filtered": filtered}
    if collab_warning:
        response_payload["warnings"] = [collab_warning]
    if include_raw:
        response_payload["raw"] = {
            "repo": repo_data,
            "collaborators": safe_json(collab_response) or [],
        }

    return jsonify(response_payload)


@app.route("/api/commit-count", methods=["POST"])
def commit_count():
    payload = request.get_json(silent=True) or {}
    repo_input = (payload.get("repo") or "").strip()
    token = (payload.get("token") or os.getenv("GITHUB_TOKEN") or "").strip()

    parsed = parse_repo_identifier(repo_input)
    if not parsed:
        return (
            jsonify({"error": "Invalid repo format. Use owner/repo or a GitHub URL."}),
            400,
        )

    owner, repo = parsed
    headers = build_headers(token)
    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    repo_response = requests.get(repo_url, headers=headers, timeout=15)
    if repo_response.status_code != 200:
        message = None
        repo_body = safe_json(repo_response)
        if isinstance(repo_body, dict):
            message = repo_body.get("message")
        return (
            jsonify(
                {
                    "error": "GitHub repo request failed.",
                    "status_code": repo_response.status_code,
                    "message": message or repo_response.text.strip(),
                }
            ),
            repo_response.status_code,
        )

    count, response = fetch_commit_count(owner, repo, headers)
    if count is None:
        message = None
        body = safe_json(response)
        if isinstance(body, dict):
            message = body.get("message")
        return (
            jsonify(
                {
                    "error": "GitHub commit request failed.",
                    "status_code": response.status_code,
                    "message": message or response.text.strip(),
                }
            ),
            response.status_code,
        )

    return jsonify(
        {"owner": owner, "repoName": repo, "commitCount": count}
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
