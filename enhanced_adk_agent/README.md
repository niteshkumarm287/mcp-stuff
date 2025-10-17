# **Stage 2: Sequential Agent + MCP Integration**

Stage 2 is about **taking your Stage 1 summarizer** and making it **modular, self-improving, and capable of multi-step reasoning**.

---

## **1️⃣ Objective of Stage 2**

* Stage 1 is a **single-agent, prompt-driven summarizer**.
* Stage 2 introduces **multi-agent orchestration**:

  1. **SequentialAgent pipeline** – chains multiple agents together.
  2. **Critic / MCP agent** – automatically reviews and improves outputs.
  3. Optional: **Rewriter agent** – applies critique feedback for a refined summary.

**Goal:**

* Instead of producing only one summary, the system now **summarizes → critiques → improves**.
* Mimics a **human workflow**: writer → editor → final review.

---

## **2️⃣ How Stage 2 Works Conceptually**

### **Pipeline Flow**

```
           ┌──────────────┐
           │  Input Text  │
           └─────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ SummarizerAgent │  Stage 1 agent
        │  (root_agent)   │
        └─────┬───────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Critic / MCP    │  Stage 2 agent
        │   Evaluates     │
        │  the summary    │
        └─────┬───────────┘
                 │
          ┌──────┴───────┐
          │ Rewriter /   │
          │ Improved     │
          │ Summary      │
          └──────────────┘
```

---

### **3️⃣ Roles of Agents**

| Agent                 | Role in Stage 2                                                                                       |
| --------------------- | ----------------------------------------------------------------------------------------------------- |
| **SummarizerAgent**   | Generates the initial summary from the input text (Stage 1 agent).                                    |
| **CriticAgent (MCP)** | Reviews the summary for clarity, conciseness, coherence, and factual accuracy. Suggests improvements. |
| **RewriterAgent**     | Produces an improved version of the summary based on critique feedback.                               |

> This demonstrates the **MCP pattern**: **Model → Critique → Improve**.

---

### **4️⃣ Why This Stage Matters**

* Stage 1 outputs are **prompt-driven but static**, with no internal feedback.

* Stage 2 introduces **self-review and iterative improvement**, which is critical for:

  * High-quality summarization at scale
  * Error detection and correction
  * Multi-step reasoning pipelines

* **ADK’s SequentialAgent** allows chaining agents while preserving context across stages.

---

### **5️⃣ Components Used in Stage 2**

| Component                   | Purpose                                               |
| --------------------------- | ----------------------------------------------------- |
| **SequentialAgent**         | Orchestrates multiple agents in a pipeline.           |
| **MCP (CriticAgent)**       | Evaluates outputs and suggests refinements.           |
| **root_agent (Summarizer)** | Stage 1 agent integrated into the pipeline.           |
| **ADK CLI / Web UI**        | Test and visualize the sequential pipeline.           |
| **JSON input**              | Structured input for multiple agents in the pipeline. |

---

### **6️⃣ Example Flow in Code**

```python
from google.adk.agents import LlmAgent, SequentialAgent

# Stage 1: Summarizer
summarizer = LlmAgent(
    name="summarizer_agent",
    model="gemini-2.5-flash",
    instruction="Summarize the text concisely..."
)

# Stage 2: Critic (MCP)
critic = LlmAgent(
    name="critic_agent",
    model="gemini-2.5-flash",
    instruction="Review the summary for clarity, coherence, and conciseness."
)

# Stage 2: Optional Rewriter
rewriter = LlmAgent(
    name="rewriter_agent",
    model="gemini-2.5-flash",
    instruction="Use critique feedback to improve the summary."
)

# Sequential pipeline using correct 'sub_agents' parameter
pipeline = SequentialAgent(
    name="summarizer_pipeline",
    description="Pipeline: Summarize → Critique → Improve",
    sub_agents=[summarizer, critic, rewriter]
)
```

* **SequentialAgent** automatically passes outputs from one agent to the next.
* You can optionally **wrap each agent to capture intermediate outputs** for debugging or analysis.

---

### **7️⃣ Benefits of Stage 2**

1. **Modular design** – add/remove agents easily.
2. **Iterative improvement** – each stage refines output.
3. **Reusability** – SummarizerAgent can be reused in multiple pipelines.
4. **Foundation for RAG / Vertex AI integration** – plug in retrieval or external context at any stage.
