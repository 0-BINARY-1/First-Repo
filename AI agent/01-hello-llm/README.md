# 01 — Hello LLM (Stage A)

Call a language model from Python. No tools. No agent loop. Just: **messages in, text out**.

## 0. Install Python (Windows)

This machine did not have `python` on PATH. Install it before anything else.

1. Download **Python 3.12+** from [python.org/downloads](https://www.python.org/downloads/).
2. Run the installer.
3. Check **Add python.exe to PATH**.
4. Close and reopen the terminal.
5. Confirm:

```powershell
python --version
pip --version
```

You want 3.11 or newer. If Windows opens the Microsoft Store instead, turn off the `python.exe` App execution alias under **Settings → Apps → Advanced app settings → App execution aliases**.

Get an API key from [OpenAI API keys](https://platform.openai.com/api-keys). You will need a billed account; set a monthly usage limit in the dashboard.

## 1. Create a virtual environment

In this folder:

```powershell
cd "F:\AI agent\01-hello-llm"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again.

## 2. Add your key

```powershell
copy .env.example .env
```

Open `.env` and paste your real key. Do not share it. Do not commit it.

## 3. Run one question

```powershell
python main.py
```

Change the **system prompt** (this is the “change it twice” exercise):

```powershell
python main.py --style tutor
python main.py --style poet
```

Ask your own question:

```powershell
python main.py "What is JSON, in two sentences?"
```

Look at the token line at the bottom. That is usage (and cost).

## 4. Run a real conversation

```powershell
python chat.py
```

Ask something, then a follow-up that only makes sense with history (for example: “make that even shorter”). Type `quit` to exit.

If follow-ups work, you now understand **short-term memory**: it is just the `messages` list you keep sending.

## What you should be able to explain

- Difference between `system` and `user`
- Why `temperature=0.2` makes answers more stable
- Why tokens matter
- Why this is still **not** an agent

Next folder: `02-json-clerk` (Stage B — structured output).
