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
        async with httpx.AsyncClient(follow_redirects=True) as client:
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
        
    async def get_file_content(self, repo_name: str, file_path: str) -> tuple[str, str]:
        url = f"{self.base_url}/repos/{repo_name}/contents/{file_path}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 404:
                return "", ""
            data = response.json()
            import base64
            content = base64.b64decode(data["content"]).decode("utf-8")
            sha = data["sha"]
            return content, sha

    async def update_file_content(self, repo_name: str, file_path: str, content: str, sha: str, commit_message: str):
        url = f"{self.base_url}/repos/{repo_name}/contents/{file_path}"
        import base64
        encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        body = {
            "message": commit_message,
            "content": encoded,
        }
        if sha:
            body["sha"] = sha
        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=self.headers, json=body)
            return response.json()