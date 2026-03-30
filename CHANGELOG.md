## [2026-03-30] - PR #3

**fix: ground agent prompts to prevent file hallucination**

This PR modifies the agent's system prompt generation by dynamically fetching `files` using `get_files_in_directory` based on `agent_config["grounding_directory"]`. These `files` are formatted into an `allowed_files` string, replacing a `repo_name` placeholder in the `system_prompt`. This change grounds the agent with concrete file context, preventing hallucination of non-existent files and improving reliability.

**Files changed:** None explicitly mentioned in summary.
**Type:** bugfix

---

## [2026-03-30] - PR #2

**feat: add two-node LangGraph pipeline with changelog writer**

Introduced a two-node LangGraph pipeline to automate changelog generation using an LLM agent. This pipeline reads PR data and existing changelogs via new tools, then writes updated entries to a file, enhancing documentation consistency and reducing manual effort.

**Files changed:** src/langchain_tools.py, src/llm.py, src/prompts.py, src/state.py, src/graph.py, src/main.py
**Type:** feature

