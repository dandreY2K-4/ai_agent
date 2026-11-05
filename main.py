import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable wasn't found.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
            }
        ],
    )

    if not response.usage:
        raise RuntimeError(
            "idk man, for some reason tokens were None... check it out and good luck."
        )

    x = response.usage.prompt_tokens
    y = response.usage.completion_tokens

    print(f"Prompt tokens: {x}")
    print(f"Response tokens: {y}")
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
