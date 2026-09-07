# Learn AI Agents: A Practical Path for Beginners

This guide assumes **basic programming knowledge** (variables, functions, if/else, loops, and reading simple code). You do **not** need a machine-learning degree. You will learn by building small things, not by collecting theory.

**Goal:** by the end, you can explain how an agent works, call an LLM from code, give it tools, and ship a small agent that does a real job.

---

## 1. What you are actually building

An **AI model** (like GPT, Claude, Gemini) is a text engine. You send text in; it sends text out.

An **AI agent** is a **loop** around that engine:

1. Receive a goal (“summarize this PDF”, “answer from my notes”, “book a meeting”).
2. Think: decide the next step.
3. Act: call a **tool** (search, read a file, run code, hit an API).
4. Observe the result.
5. Repeat until the goal is done or it must stop.
6. Return a final answer.

If there is no loop and no tools, you have a **chatbot**, not an agent. Chatbots are still useful; agents are chatbots plus **actions** and **control**.

```
User goal
    │
    ▼
┌──────────────┐
│  LLM (brain) │◄──── memory / history
└──────┬───────┘
       │ decide: answer or use a tool
       ▼
┌──────────────┐
│ Tools (hands)│  files, APIs, search, code
└──────┬───────┘
       │ result
       ▼
   loop again or finish
```

Keep this picture in your head. Every framework (LangChain, CrewAI, OpenAI Agents SDK, etc.) is just a nicer way to write this loop.

---

## 2. Mindset before you write code

Treat this like learning web development, not like “becoming an ML researcher.”

| You need | You do **not** need first |
|----------|---------------------------|
| Clear Python | Training neural nets from scratch |
| HTTP / APIs | Linear algebra |
| Structured prompting | Fine-tuning GPUs |
| Debugging logs | A huge dataset |

**Rule:** always know *who is in control*. The model suggests; **your code** decides which tools exist, what data it can see, and when to stop. Never let an agent run unbounded or write/delete files without limits.

---

## 3. Setup (do this once)

### 3.1 Language

Use **Python 3.11+**. Almost every agent tutorial, SDK, and example is Python-first.

Install:

- [Python](https://www.python.org/downloads/)
- A code editor (Cursor, VS Code, or similar)
- `pip` (comes with Python)

Check:

```bash
python --version
pip --version
```

### 3.2 Virtual environment

Never install packages into the global Python. In a project folder:

```bash
python -m venv .venv
```

Activate:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS / Linux: `source .venv/bin/activate`

Then:

```bash
pip install openai python-dotenv
```

### 3.3 API key

You need access to a model. Pick **one** to start:

| Provider | Typical use |
|----------|-------------|
| OpenAI | GPT models, large ecosystem |
| Anthropic | Claude, strong at long context and tools |
| Google | Gemini |
| Local (Ollama) | Free, private, weaker / slower on a laptop |

Create a `.env` file (never commit this file):

```
OPENAI_API_KEY=sk-your-key-here
```

Load it in Python:

```python
from dotenv import load_dotenv
load_dotenv()
```

**Cost habit:** start with a cheap/fast model for experiments. Log every call. Set a monthly spend cap in the provider dashboard.

---

## 4. Learning path (follow in order)

Do not skip ahead to multi-agent frameworks. That is how people get confused.

| Stage | Outcome | Time (rough) |
|-------|---------|--------------|
| A. Chat completions | You can call a model from Python | 1–2 days |
| B. Prompting | You get reliable, structured answers | 2–3 days |
| C. Tools | The model can call *your* functions | 3–5 days |
| D. Agent loop | You write the think–act–observe loop | 3–5 days |
| E. Memory & RAG | The agent uses *your* documents | 1 week |
| F. One real product | A small agent you would actually use | 1–2 weeks |
| G. Frameworks | You choose a library with eyes open | after F |

---

## 5. Stage A — Talk to a model from code

This is the foundation. If this is shaky, everything later will feel like magic.

**Concepts:**

- **Prompt** = the text you send.
- **Completion / response** = the text you get back.
- **Tokens** ≈ pieces of words. You pay per token. Context has a max size.
- **Temperature** = randomness. Low = more predictable. High = more creative, less reliable.
- **System vs user messages** = “who you are / rules” vs “this request.”

**Minimal example (OpenAI-style):**

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",  # use whatever cheap model your account has
    messages=[
        {"role": "system", "content": "You are a concise programming tutor."},
        {"role": "user", "content": "Explain what an API is in 3 sentences."},
    ],
    temperature=0.2,
)

print(response.choices[0].message.content)
```

**Exercises:**

1. Change the system prompt and see how the tone changes.
2. Ask a follow-up by appending another `user` message **and** the previous assistant message (that is conversation history).
3. Print `response.usage` so you see token counts.

**Checkpoint:** you can send a question, get an answer, and explain what `messages` is.

---

## 6. Stage B — Prompting that actually works

Prompting is not poetry. It is **specifying a job**.

A solid prompt includes:

1. **Role** — who the model is.
2. **Goal** — what success looks like.
3. **Constraints** — length, format, what not to do.
4. **Input** — the data.
5. **Output shape** — JSON, bullets, a table, a function call.

**Bad:** “Write something about agents.”

**Better:**

```
You extract action items from meeting notes.

Rules:
- Return JSON only.
- Schema: {"items": [{"owner": string, "task": string, "due": string | null}]}
- If a field is unknown, use null. Do not invent due dates.

Notes:
"""
...paste notes...
"""
```

**Techniques worth learning (in this order):**

1. **Zero-shot** — just ask clearly.
2. **Few-shot** — show 1–3 examples of good input/output.
3. **JSON / schema** — force a structure your code can parse.
4. **Chain of thought (careful)** — ask for reasoning *internally*, then a short final answer. Do not dump long reasoning to users unless you need it.
5. **Eval a prompt** — keep 10 test inputs. If you change the prompt, re-run all 10.

**Exercise:** take messy emails and extract `{sender, intent, urgency}` as JSON. Parse with `json.loads`. If parsing fails, retry once with “fix the JSON.”

**Checkpoint:** your code can *rely* on the output format, not just print pretty text.

---

## 7. Stage C — Tools (this is where agents start)

A **tool** is a Python function the model is *allowed* to request.

Example tools:

- `get_weather(city)`
- `read_file(path)` (only inside a safe folder)
- `search_notes(query)`
- `create_calendar_event(...)`

The model does **not** execute Python by itself. It returns something like: “call `get_weather` with `city=Kathmandu`.” **Your code** runs the function and sends the result back.

**Mental model:**

```
You: "What's the weather in Kathmandu?"
Model: tool_call get_weather("Kathmandu")
Your code: runs function → "24°C, cloudy"
Model: "It's 24°C and cloudy in Kathmandu."
```

**Design rules for tools:**

- One tool = one clear job.
- Names and descriptions must be precise; the model chooses tools from those descriptions.
- Validate arguments. Never trust the model with raw paths, SQL, or shell commands.
- Return short, factual strings or JSON. Do not return novels.
- Prefer **read-only** tools first. Write/delete tools need extra confirmation.

**Exercise:** write `add(a, b)` and `multiply(a, b)`. Ask: “What is (12 + 7) * 3?” The model must use tools, not guess.

**Checkpoint:** you have at least two functions registered, and you can see the model *choose* them in logs.

---

## 8. Stage D — The agent loop (write it yourself once)

Before LangChain or CrewAI, write a **tiny loop**. This is the most important skill in this whole document.

Pseudo-code:

```python
messages = [system, user_goal]

for step in range(MAX_STEPS):  # hard stop, e.g. 8
    response = llm(messages, tools=TOOLS)

    if response.wants_to_call_a_tool:
        result = run_tool(response.tool_name, response.tool_args)
        messages.append(tool_result)
        continue

    # no tool → final answer
    return response.text

return "Stopped: too many steps."
```

**You must implement:**

- `MAX_STEPS` so it cannot loop forever
- logging of every thought / tool / result
- a tool allowlist
- error handling (“tool failed: …”) so the model can recover

**First agent project (do this):**

**Research-and-summarize agent**

- Tools: `web_search(query)` (or a fake search over a local JSON file if you have no search API), `fetch_url(url)` (optional).
- Goal: “Answer this question with 3 bullet facts and sources.”
- Stop after N searches.

If you cannot call the web yet, **fake the tools** with a local `articles.json`. The loop is the lesson, not Google.

**Checkpoint:** you can draw the loop on paper and point to the matching lines in your script.

---

## 9. Stage E — Memory, files, and RAG

Models forget everything between sessions unless **you** store it.

### 9.1 Short-term memory

The `messages` list *is* short-term memory. It grows. Long chats hit token limits and get expensive.

**Simple tactics:**

- Keep only the last N turns.
- After each session, write a 5-line summary and start the next chat with that summary.

### 9.2 Long-term memory

A database or files: user preferences, past tasks, notes.

Start with JSON or SQLite. Do not start with a vector database on day one.

### 9.3 RAG (Retrieval-Augmented Generation)

RAG means: **find relevant chunks of *your* data, then put them in the prompt.**

Typical pipeline:

1. Split documents into chunks (e.g. 300–800 words with overlap).
2. Embed each chunk (turn text into a list of numbers).
3. On a question, embed the question, find nearest chunks.
4. Prompt: “Answer using only these excerpts. If missing, say you don’t know.”

**When you need RAG:** the knowledge is too large or too private to paste every time (company docs, your notes, PDFs).

**When you don’t:** a 3-page policy; just paste it.

**First RAG project:** put 5 markdown notes in a folder. Ask questions that only those notes can answer. Verify it cites the right note.

Libraries you will meet later: embeddings APIs, Chroma, FAISS, LlamaIndex. Learn the *idea* first.

**Checkpoint:** you can explain RAG in one sentence: *search your docs, then generate from the hits.*

---

## 10. Stage F — Ship one useful agent

Pick **one** personal or work problem. Constraints:

- You would use it weekly.
- It has 2–5 tools, not 20.
- Success is measurable (correct JSON, saved file, sent draft).

**Good first products:**

| Agent | Tools | Why it’s good |
|-------|-------|----------------|
| Meeting-notes → action items | parse text, write markdown | Clear I/O |
| Personal knowledge Q&A | RAG over your notes | Teaches retrieval |
| Inbox triage (draft only) | classify + draft reply | No auto-send |
| File organizer | list files, propose moves | Human confirms writes |
| Study tutor | quiz from a PDF + score answers | Tight loop |

**Bad first products:**

- “Autonomous company CEO”
- Unrestricted computer-use agent
- Anything that sends email or spends money without approval

**Ship checklist:**

- [ ] README: how to run, what keys are needed
- [ ] `.env.example` with dummy keys
- [ ] Max steps + logging
- [ ] A folder the agent is allowed to touch
- [ ] 5 test questions with expected behavior

---

## 11. Stage G — Frameworks (after you can write the loop)

Frameworks save time. They also hide the loop. Learn them **after** Stage D.

| Tool / stack | Use when |
|--------------|----------|
| Provider SDKs (OpenAI, Anthropic, Google) | You want control and fewer layers |
| **OpenAI Agents SDK** / similar official agent APIs | Structured tools + tracing from the vendor |
| **LangChain** | Lots of integrations; can get abstract |
| **LangGraph** | You need explicit state machines / graphs |
| **LlamaIndex** | Document-heavy RAG |
| **CrewAI** | Multiple roles (researcher, writer) — easy to overuse |
| **Pydantic** / **Instructor** | Reliable structured output |
| **FastAPI** | Turn the agent into an HTTP API |
| **Ollama** | Local models, no API bill |

**Advice:** build your first two agents with the raw SDK. Then rebuild one in a framework and notice what the framework did for you.

---

## 12. How modern agent systems are usually designed

When you read blogs or GitHub repos, map them to these pieces:

1. **Planner** — break a goal into steps (sometimes the same LLM).
2. **Executor** — run tools.
3. **Memory** — history + long-term store.
4. **Retriever** — RAG.
5. **Guardrails** — validation, allowlists, PII filters, human approval.
6. **Orchestrator** — the loop or graph that ties it together.
7. **Observability** — traces of prompts, tools, tokens, failures.

**Multi-agent** (researcher + critic + writer) is optional. One competent agent with good tools beats five confused agents. Add a second agent only when roles truly conflict (e.g. “generate” vs “strictly review”).

---

## 13. Evaluation, debugging, and quality

Agents fail in boring ways: bad tool descriptions, bloated context, no stop condition, hallucinated facts.

**Debug like an engineer:**

- Log: user input, model output, tool name, tool args, tool result, token usage.
- Reproduce with `temperature=0` when possible.
- Keep a **golden set** of 10–20 tasks. Run them after every prompt change.

**What “good” means:**

- Task success rate (did it finish correctly?)
- Tool error rate
- Average steps / cost
- Hallucination rate on questions that should be “I don’t know”

If you cannot measure it, you are demoing, not engineering.

---

## 14. Safety and professionalism (non-negotiable)

You are responsible for what the agent *does*, not only what it *says*.

- **Secrets:** API keys in `.env` only. Never paste keys into prompts or git.
- **Least privilege:** tools can only do what the job needs.
- **Human in the loop** for send, pay, delete, deploy.
- **Prompt injection:** untrusted web pages / emails can say “ignore your instructions.” Treat retrieved text as *data*, not as commands.
- **Copyright and privacy:** don’t dump other people’s private data into a public model without permission.
- **Local vs cloud:** sensitive data → local models or a provider with a data-use policy you accept.

---

## 15. Suggested 4-week plan

Assume 60–90 minutes a day. Adjust freely.

### Week 1 — Model as a function

- Days 1–2: Python refresh (functions, dicts, JSON, files, `venv`).
- Days 3–4: Stage A — chat completions, history, tokens.
- Day 5: Stage B — JSON extraction project.
- Weekend: write a one-page note: “What is a token, a prompt, and a tool?”

### Week 2 — Tools and the loop

- Days 1–3: Stage C — calculator / weather / file-read tools.
- Days 4–5: Stage D — your own agent loop with `MAX_STEPS`.
- Weekend: research-and-summarize agent (even with fake search).

### Week 3 — Memory and RAG

- Days 1–2: chat summarization + SQLite notes.
- Days 3–5: Stage E — chunk, embed, retrieve, answer from notes.
- Weekend: Q&A over your own markdown files.

### Week 4 — Product

- Days 1–4: Stage F — one real agent, README, tests.
- Day 5: add logging and a FastAPI or CLI wrapper.
- After that: peek at one framework (Stage G) and rebuild a slice.

---

## 16. Python you should be comfortable with

If any of these feel rusty, practice them *before* agents:

- Functions, `*args` / kwargs, type hints (`def f(x: str) -> dict`)
- Lists, dicts, list comprehensions
- `json.loads` / `json.dumps`
- Reading/writing files, `pathlib`
- `try/except`
- Virtualenv and `pip`
- HTTP: what GET/POST and JSON APIs are (`httpx` or `requests`)

Optional but useful soon: classes, `asyncio`, Pydantic models.

---

## 17. Mini-syllabus of projects (do them in order)

1. **Echo tutor** — Q&A with a system prompt. No tools.
2. **JSON clerk** — extract structured data from messy text.
3. **Tool calculator** — add/multiply via tools.
4. **File Q&A (no RAG)** — paste one document into the prompt.
5. **Your agent loop** — fake search + summarize.
6. **Notes RAG** — folder of markdown files.
7. **CLI agent** — `python agent.py "your goal"` with logging.
8. **Approved writer** — drafts a file; you type `yes` before write.

Each project should be a **new folder** with `README.md`, `.env.example`, and `main.py`.

---

## 18. How to study (so you don’t drown)

The field is noisy. Filter hard.

**Do:**

- Read official SDK docs for *one* provider.
- Rebuild examples from scratch without copy-paste.
- Follow one course or book at a time (see below), then stop collecting links.

**Don’t:**

- Install five agent frameworks in one weekend.
- Start with “fully autonomous computer use.”
- Fine-tune a model before you have a working tool-using agent.

When a new paper or product appears, ask: *does this change the loop, the tools, or the memory?* If no, you can ignore it for now.

---

## 19. Curated resources (start here, not everywhere)

Use these as **references**, not as a second full-time job.

**Concepts**

- [OpenAI — intro to language models and prompting](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic — prompt engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Google — prompting / Gemini API docs](https://ai.google.dev/gemini-api/docs)

**Agents and tools**

- Your chosen provider’s **function calling / tools** docs (search “function calling” + provider name)
- [LangGraph docs](https://langchain-ai.github.io/langgraph/) — when you need graphs
- [LlamaIndex docs](https://docs.llamaindex.ai/) — when you need RAG depth

**Local models**

- [Ollama](https://ollama.com/)

**Engineering habits**

- Learn to read traces: input tokens, tool calls, failures.
- [12-factor app](https://12factor.net/) ideas still apply: config in env, logs as streams.

Replace any dead link with the provider’s current “Get started” page. APIs change; the **loop** does not.

---

## 20. Glossary

| Term | Meaning |
|------|---------|
| **LLM** | Large language model — the text engine |
| **Agent** | LLM + loop + tools + stop conditions |
| **Tool / function calling** | Model requests a function; your code runs it |
| **Context window** | Max tokens the model can see at once |
| **Hallucination** | Confident wrong output |
| **RAG** | Retrieve your docs, then generate |
| **Embedding** | Numeric fingerprint of a text chunk |
| **Prompt injection** | Malicious text that tries to override instructions |
| **Fine-tuning** | Training the model on extra examples — *not* your first step |
| **Temperature** | Randomness of sampling |
| **Orchestration** | Code that runs the loop / graph |

---

## 21. What “good enough to call yourself an agent builder” looks like

You can:

1. Call an LLM from Python and manage message history.
2. Force structured JSON output and parse it.
3. Register tools and run a bounded think–act–observe loop.
4. Add retrieval over a small personal corpus.
5. Log cost, steps, and failures.
6. Explain every line of *your* agent without waving at a framework.

When you can do that, you are no longer a beginner. Next skills (APIs, auth, eval harnesses, graphs, multi-agent, fine-tuning) will attach to this core instead of replacing it.

---

## 22. Start tomorrow morning

Do only this:

1. Create a folder `01-hello-llm`.
2. Make a venv, add `.env` with one API key.
3. Run the Stage A script. Change the system prompt twice.
4. Write three sentences in a `notes.md`: what a message, a token, and a tool are.

That is the real start. Everything else in this file is the map for the weeks after.
