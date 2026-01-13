import os
import sys
from google import genai
from google.genai import types, errors
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()

    args = sys.argv[1:]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if not args:
        run_token_demo(client)
        return
    #     print("AI Code Assistant")
    #     print('\nUsage: python main.py "your prompt here"')
    #     print('Example: python main.py "How do I build a calculator app?"')
    #     sys.exit(1)
    
    verbose = False
    if "--verbose" in args:
        verbose = True
        verbose_flag = args.index("--verbose")
        del args[verbose_flag]

    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if verbose:
        print(f"User prompt: {user_prompt}")

    try:
        generate_content(client, messages, verbose)
    except errors.ClientError as err:
        print(str(err))


def generate_content(client, messages, verbose):
    timeout = 20
    while timeout != 0:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )
        )
        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError("No usage metadata returned from Gemini API")

        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls:
            for function_call_part in response.function_calls:
                try:
                    function_call_result = call_function(function_call_part, verbose)
                    messages.append(function_call_result)
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                except:
                    raise Exception("Failed to match funtion to request")
        else:
            print(response.text)
            break

        timeout -= 1

# Fucntion for lesson update after AI agent module was completed
def run_token_demo(client):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
