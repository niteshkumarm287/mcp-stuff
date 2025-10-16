## Stage 1 Summarizer Agent Workflow

```
            ┌─────────────────────────────┐
            │  User / Client Input JSON   │
            │  {"text": "..."}           │
            └─────────────┬─────────────┘
                          │
                          ▼
             ┌───────────────────────────┐
             │   ADK Web UI / CLI        │
             │ uv run adk web            │
             │ Loads agent modules       │
             └─────────────┬────────────┘
                           │
                           ▼
             ┌───────────────────────────┐
             │  Python Agent Module      │
             │  summarizer_agent.agent   │
             │                           │
             │  ┌─────────────┐          │
             │  │ root_agent  │  ──────────► LlmAgent executes
             │  └─────────────┘          │  instructions on input
             └─────────────┬────────────┘
                           │
                           ▼
             ┌───────────────────────────┐
             │  LLM Model (Gemini 2.5)  │
             │  - Processes text         │
             │  - Applies instructions   │
             │  - Generates summary      │
             └─────────────┬────────────┘
                           │
                           ▼
             ┌───────────────────────────┐
             │ Output JSON / Summary     │
             │ Delivered via Web UI      │
             │ {"summary": "..."}       │
             └───────────────────────────┘
```

---

### Step-by-Step Explanation

1. **User / Client Input**

   * JSON object is sent to the agent, containing the text to summarize.

2. **ADK Web UI / CLI**

   * The ADK runtime (`uv run adk web`) loads all modules in `summarizer_agent`.
   * Detects `root_agent` automatically.

3. **Python Agent Module (`summarizer_agent.agent`)**

   * Contains your `root_agent` instance of `LlmAgent`.
   * This object defines the **model** (`gemini-2.5-flash`) and **instructions** (how to summarize text).

4. **LLM Model Execution**

   * The `LlmAgent` passes the text and instructions to the underlying **Gemini 2.5 model**.
   * Model generates a summary following your instructions.

5. **Output Delivery**

   * The summary is returned as JSON.
   * Displayed in the **web UI** or can be retrieved programmatically if needed.

---

### Key Takeaways

* `root_agent` is the **entry point** for ADK to discover your agent.
* All execution (input → LLM → output) is **managed internally by ADK**.
* No manual session or async handling is required for a single-agent Stage 1 setup.
* This workflow can be **extended** to SequentialAgents, MCP, and RAG stages later.

