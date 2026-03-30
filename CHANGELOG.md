## [2026-03-30] - PR #2

**feat: add two-node LangGraph pipeline with changelog writer**

Introduced a two-node LangGraph pipeline to automate changelog generation using an LLM agent. This pipeline reads PR data and existing changelogs via new tools, then writes updated entries to a file, enhancing documentation consistency and reducing manual effort.

**Files changed:** src/langchain_tools.py, src/llm.py, src/prompts.py, src/state.py, src/graph.py, src/main.py
**Type:** feature

