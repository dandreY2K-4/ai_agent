import argparse
import json
import os

from call_function import available_functions
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
        tools=available_functions,  # type: ignore
    )

    if not response.usage:
        raise RuntimeError(
            "idk man, for some reason tokens were None... check your key or something and good luck."
        )

    if verbose:
        print(
            f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}\n"
        )

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")  # type: ignore
            print(f"Calling function: {tool_call.function.name}({function_args})")  # type: ignore

    print(f"Response:\n{response.choices[0].message.content}")


if __name__ == "__main__":
    main()
