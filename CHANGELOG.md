## [2026-03-30] - PR #3

**fix: ground agent prompts to prevent file hallucination**

This PR updates the prompt templates in `app/agents/doc_agent.py` for the `analyze_diff` and `write_changelog` functions. It embeds new "CRITICAL RULES" to restrict AI agents to referencing only explicitly visible files and structures in diffs or summaries. This change prevents hallucination, enhancing the accuracy and reliability of generated code analysis and changelog entries.

**Files changed:** app/agents/doc_agent.py
**Type:** bugfix

## [2026-03-30] - PR #3

**fix: ground agent prompts to prevent file hallucination**

Refactored agent chat completion by delegating system prompt construction to a new `agentChatCompletionStream` function exported from `src/lib/agent/index.ts`. This stream utilizes `buildGroundingSystemPrompt` from `src/lib/agent/prompt.ts` to create a robust system prompt with explicit instructions. This change, reflected in `src/components/chat/use-chat.ts`, prevents AI hallucination of file names and content by explicitly grounding agent responses.

**Files changed:** src/components/chat/use-chat.ts, src/lib/agent/index.ts, src/lib/agent/prompt.ts
**Type:** bugfix

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

