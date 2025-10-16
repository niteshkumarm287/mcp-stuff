# Summarizer Agent using Google Cloud ADK

## Overview

The `summarizer_agent` project demonstrates how to build a **text summarization agent** using the **Google Cloud Agent Development Kit (ADK) v1.16**.

This agent takes raw text and produces concise, coherent summaries that **capture key information, preserve context, and remove unnecessary redundancy**. It is designed as a **Stage 1 prototype**, forming the foundation for more advanced pipelines like **Sequential Agents, MCP, and RAG integration**.

---

## Folder Structure

```
.
├── main.py                 # Optional script for local testing
├── summarizer_agent/
│   ├── __init__.py         # Marks the module
│   └── agent.py            # Defines the root_agent (core agent)
├── .venv/                  # Python virtual environment
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file (UV / ADK)
└── README.md               # This documentation
```

---

## How It Works

### Agent Definition

The agent is defined in `summarizer_agent/agent.py`:

```python
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name='summarizer_agent',
    model='gemini-2.5-flash',
    description='An agent that creates clear, concise summaries of text while preserving key information and context.',
    instruction=''' ...summarization instructions... '''
)
```

**Key Points:**

* **`root_agent`**

  * Required at the **module level** for ADK runtime discovery.
  * The CLI (`uv run adk web`) automatically detects this variable.

* **`LlmAgent`**

  * Represents a single AI agent that can process instructions.
  * Handles text summarization using **Gemini 2.5 Flash**, a high-quality LLM.

* **`instruction`**

  * Provides a **rich multi-step prompt** guiding the agent.
  * Ensures output is:

    * Concise and coherent
    * Factually accurate
    * Free of unnecessary information

---

### Execution

#### 1. Run via ADK Web UI (Recommended)

```bash
uv run adk web
```

* Opens a local web interface at `http://localhost:8000`.
* The `summarizer_agent` appears automatically.
* Input JSON:

```json
{"text": "Your text to summarize goes here."}
```

* The agent produces a concise summary.

---

### Why This Approach Works

1. **No direct function calls**

   * In ADK v1.16, `LlmAgent` **cannot be called like a function** (`agent(text)` fails).
   * The runtime executes the agent internally.

2. **Module-level `root_agent` is mandatory**

   * Allows ADK to discover your agent automatically without extra configuration.

3. **Web UI handles async internally**

   * No need for `InMemoryRunner`, session creation, or explicit async code.
   * Simplifies Stage 1 experimentation.

---

### Why We Use These Modules

| Module                       | Purpose                                                    |
| ---------------------------- | ---------------------------------------------------------- |
| `google.adk.agents.LlmAgent` | Defines an AI agent with instructions and model.           |
| `google.adk.agents.Agent`    | Base agent class (optional for inheritance or extensions). |

> No other modules are required for Stage 1 — the simplicity allows you to focus on **defining rich instructions and testing the agent quickly**.

---

### Key Learnings

1. **ADK v1.16** changed how agents are executed:

   * `start()` and `adk.run()` no longer exist.
   * `uv run adk local` is deprecated; only `uv run adk web` is supported.
2. **`root_agent` is required** at the module level.
3. **Instructions drive agent behavior** — the clearer and more structured, the better the summarization.

---

## References

* [Google ADK Documentation](https://google.github.io/adk-docs/)
* [Gemini LLM Models](https://cloud.google.com/genai)

