import argparse
import os

from call_function import available_functions, call_function
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from sys import exit

MAX_I = 20  

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

    for _ in range(MAX_I):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({MAX_I}) reached")
    exit(1)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> str | None:

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
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}\n")

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        tool_message = call_function(tool_call=tool_call, verbose=verbose)
        if not tool_message.get("content"):
            raise RuntimeError(f"No function was called by {tool_call.function.name}.")
        if verbose:
            print(f"-> {tool_message['content']}")
        messages.append(tool_message)

    return None


if __name__ == "__main__":
    main()
