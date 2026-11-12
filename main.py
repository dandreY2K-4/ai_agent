import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "user_prompt",
        type=str,  # CAREFUL, last time this causes an error of some kind
        help="'user_prompt': Type your prompt to the chatbot right after 'main.py'.",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable wasn't found.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    user_content = args.user_prompt
    verbose = args.user_prompt
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    if verbose:
        print(f"User prompt: {user_content}\n")

    generate_content(client=client, messages=messages, verbose=verbose)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> None:

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if not response.usage:
        raise RuntimeError(
            "idk man, for some reason tokens were None... check your key or something and good luck."
        )

    x = response.usage.prompt_tokens
    y = response.usage.completion_tokens

    if verbose:
        print(f"Prompt tokens: {x}\nResponse tokens: {y}\n")

    print(f"Response:\n{response.choices[0].message.content}")


if __name__ == "__main__":
    main()
