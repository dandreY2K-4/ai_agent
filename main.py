import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable wasn't found.")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "user_prompt",
        help="'user_prompt': Type your prompt to the chatbot right after 'main.py'.",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")

    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    generate_content(args=args, client=client)


def generate_content(args: argparse.Namespace, client: OpenAI):

    # Next lines where declare role, content, message and response could be
    # placed outside the func and message be passed as input instead of args.
    role = "user"
    content = args.user_prompt
    messages = [{"role": role, "content": content}]

    response = client.chat.completions.create(
        model="openrouter/free", messages=messages  # type: ignore
    )

    if not response.usage:
        raise RuntimeError(
            "idk man, for some reason tokens were None... check it out and good luck."
        )

    x = response.usage.prompt_tokens
    y = response.usage.completion_tokens

    if args.verbose:
        print(f"User prompt: {content}\n")
        print(f"Prompt tokens: {x}")
        print(f"Response tokens: {y}\n")
        print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
