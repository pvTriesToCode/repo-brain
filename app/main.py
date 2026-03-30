from fastapi import FastAPI, Request, HTTPException, Header
import hmac
import hashlib
from app.core.config import settings
from app.services.github_service import GitHubService
from app.agents.doc_agent import doc_agent

app = FastAPI(
    title="Repo Brain",
    description="AI-powered documentation agent for GitHub repos",
    version="1.0.0"
)

github_service = GitHubService()

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    expected = hmac.new(
        settings.github_webhook_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

@app.get("/")
async def root():
    return {"status": "repo-brain is running"}

@app.post("/webhook")
async def webhook(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None)
):
    payload = await request.body()

    if not verify_webhook_signature(payload, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = await request.json()

    if x_github_event == "pull_request":
        action = data.get("action")

        if action in ["opened", "synchronize"]:
            pr_number = data["pull_request"]["number"]
            repo_name = data["repository"]["full_name"]
            diff_url = data["pull_request"]["diff_url"]
            pr_title = data["pull_request"]["title"]
            base_branch = data["pull_request"]["base"]["ref"]
            head_branch = data["pull_request"]["head"]["ref"]

            print(f"Processing PR #{pr_number} on {repo_name}")

            diff = await github_service.get_pr_diff(diff_url)

            result = doc_agent.invoke({
                "diff": diff,
                "pr_title": pr_title,
                "pr_number": pr_number,
                "repo_name": repo_name,
                "base_branch": base_branch,
                "head_branch": head_branch,
                "summary": "",
                "changelog_entry": ""
            })

            await github_service.post_or_update_comment(
                repo_name=repo_name,
                pr_number=pr_number,
                comment=result["summary"]
            )

            existing_changelog, sha = await github_service.get_file_content(
                repo_name=repo_name,
                file_path="CHANGELOG.md"
            )

            new_changelog = result["changelog_entry"] + "\n\n" + existing_changelog

            await github_service.update_file_content(
                repo_name=repo_name,
                file_path="CHANGELOG.md",
                content=new_changelog,
                sha=sha,
                commit_message=f"docs: update changelog for PR #{pr_number}"
            )

            print(f"Comment posted and changelog updated for PR #{pr_number}")

    return {"status": "received"}