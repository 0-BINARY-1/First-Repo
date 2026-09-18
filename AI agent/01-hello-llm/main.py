"""
Stage A — call a language model from Python.

A model is a function: messages in, text out.
This script is a chatbot, not an agent. No tools. No loop.
"""

import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Two system prompts. Change which one you pass with --style.
SYSTEM_PROMPTS = {
    "tutor": "You are a concise programming tutor. Use short sentences. Avoid jargon unless you define it.",
    "poet": "You are a playful poet. Answer the user's question correctly, but in 4 short lines of verse.",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Send one question to an LLM.")
    parser.add_argument(
        "question",
        nargs="?",
        default="Explain what an API is in 3 sentences.",
        help="User question to send to the model",
    )
    parser.add_argument(
        "--style",
        choices=SYSTEM_PROMPTS.keys(),
        default="tutor",
        help="Which system prompt to use",
    )
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-your-key"):
        print(
            "Missing OPENAI_API_KEY.\n"
            "1. Copy .env.example to .env\n"
            "2. Paste a real key from https://platform.openai.com/api-keys\n"
            "3. Run this script again.",
            file=sys.stderr,
        )
        sys.exit(1)

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPTS[args.style]},
        {"role": "user", "content": args.question},
    ]

    print(f"Model:  {model}")
    print(f"Style:  {args.style}")
    print(f"System: {SYSTEM_PROMPTS[args.style]}")
    print("-" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )

    print(response.choices[0].message.content)
    print("-" * 60)

    usage = response.usage
    if usage:
        print(
            f"Tokens — prompt: {usage.prompt_tokens}, "
            f"completion: {usage.completion_tokens}, "
            f"total: {usage.total_tokens}"
        )


if __name__ == "__main__":
    main()
