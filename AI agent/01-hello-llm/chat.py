"""
Stage A exercise — conversation history.

The model has no memory of past turns unless YOU send those turns
back in the messages list.
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM = "You are a concise programming tutor. Keep answers under 80 words."


def require_client() -> tuple[OpenAI, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-your-key"):
        print("Missing OPENAI_API_KEY. Copy .env.example to .env and add your key.", file=sys.stderr)
        sys.exit(1)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return OpenAI(api_key=api_key), model


def ask(client: OpenAI, model: str, messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )
    text = response.choices[0].message.content or ""
    usage = response.usage
    if usage:
        print(f"[tokens this turn: {usage.total_tokens}]")
    return text


def main() -> None:
    client, model = require_client()
    messages: list[dict] = [{"role": "system", "content": SYSTEM}]

    print("Type a question. Type 'quit' to exit.")
    print("Each reply is appended to history, so follow-up questions work.\n")

    while True:
        user = input("You: ").strip()
        if not user:
            continue
        if user.lower() in {"quit", "exit"}:
            break

        messages.append({"role": "user", "content": user})
        reply = ask(client, model, messages)
        messages.append({"role": "assistant", "content": reply})
        print(f"Tutor: {reply}\n")

    print(f"Turns stored in memory this session: {len(messages) - 1}")


if __name__ == "__main__":
    main()
