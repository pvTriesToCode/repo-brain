# 🧠 Repo Brain

An AI-powered documentation agent that automatically generates detailed PR summaries and maintains a living changelog for any GitHub repository.

## What it does

Every time a pull request is opened or updated, Repo Brain:
- Reads the full code diff
- Generates a detailed, human-readable analysis using Gemini AI
- Posts the summary as a PR comment automatically
- Appends a structured entry to `CHANGELOG.md`

## How it works

Repo Brain runs as a FastAPI service that listens to GitHub webhooks. When a PR event fires, a two-node LangGraph pipeline processes it:

1. **analyze_diff** — reads the diff and generates a deep PR summary explaining what changed, why it matters, and what reviewers should look at
2. **write_changelog** — takes that summary and writes a concise, structured changelog entry

The two nodes communicate via a shared `AgentState` object — this is the foundation of the multi-agent architecture.

## Tech stack

- **FastAPI** — webhook server
- **LangGraph** — agent orchestration
- **Gemini 2.5 Flash** — AI model
- **GitHub REST API** — fetch diffs, post comments, write files
- **Python 3.11**

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/pvTriesToCode/repo-brain.git
cd repo-brain
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_WEBHOOK_SECRET=your_webhook_secret
```

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

### 6. Expose via ngrok
```bash
ngrok http 8000
```

### 7. Configure GitHub webhook
In your repo settings → Webhooks → Add webhook:
- Payload URL: `https://your-ngrok-url/webhook`
- Content type: `application/json`
- Secret: your webhook secret
- Events: Pull requests only

## Connecting a new repo

Any GitHub repo can use Repo Brain by pointing a webhook at your deployed instance. No changes needed to the target repo's codebase.

## Roadmap

- [ ] PR Reviewer Agent — second LangGraph node that reviews code quality
- [ ] Multi-agent orchestration — documentation and reviewer agents communicate
- [ ] Persistent docs dashboard — searchable frontend for all PR summaries
- [ ] Deploy to Railway/Render for permanent public URL

## Example output

Every PR gets an automatic comment like this:

**What this PR does** — explains the architectural reasoning behind the change

**Why it matters** — business and technical value

**What changed in each file** — specific role of each modified file

**Breaking changes** — what callers need to know

**Things to look at** — specific reviewer concerns pulled from the actual code

---

Built by [Prajwal](https://github.com/pvTriesToCode)