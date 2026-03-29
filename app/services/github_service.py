import httpx
from app.core.config import settings

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {settings.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    async def get_pr_diff(self, diff_url: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                diff_url,
                headers={
                    **self.headers,
                    "Accept": "application/vnd.github.v3.diff"
                }
            )
            return response.text

    async def post_pr_comment(self, repo_name: str, pr_number: int, comment: str):
        url = f"{self.base_url}/repos/{repo_name}/issues/{pr_number}/comments"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=self.headers,
                json={"body": comment}
            )
            return response.json()

    async def get_existing_bot_comment(self, repo_name: str, pr_number: int) -> int | None:
        url = f"{self.base_url}/repos/{repo_name}/issues/{pr_number}/comments"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            comments = response.json()
            for comment in comments:
                if comment["user"]["login"] == "github-actions[bot]" or \
                   "repo-brain" in comment["body"].lower():
                    return comment["id"]
            return None

    async def update_pr_comment(self, repo_name: str, comment_id: int, comment: str):
        url = f"{self.base_url}/repos/{repo_name}/issues/comments/{comment_id}"
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                url,
                headers=self.headers,
                json={"body": comment}
            )
            return response.json()

    async def post_or_update_comment(self, repo_name: str, pr_number: int, comment: str):
        existing_id = await self.get_existing_bot_comment(repo_name, pr_number)
        if existing_id:
            return await self.update_pr_comment(repo_name, existing_id, comment)
        else:
            return await self.post_pr_comment(repo_name, pr_number, comment)