import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
    ),
)
    if response.usage_metadata is None:
        raise RuntimeError("No usage metadata")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    function_calls = response.function_calls
    function_call_result_list = []
    if function_calls:
        for function_call in function_calls:
            current_function_call_result = call_function(function_call, verbose=verbose)
            if len(current_function_call_result.parts) == 0:
                raise Exception("Parts list is empty")
            if current_function_call_result.parts[0].function_response is None:
                raise Exception("The first item in the list of parts is None")
            if current_function_call_result.parts[0].function_response.response is None:
                raise Exception("The function result is None")
            function_call_result_list.append(current_function_call_result.parts[0])
            if verbose:
                print(f"-> {current_function_call_result.parts[0].function_response.response}")
   
    return response, function_call_result_list
def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Api key not found")
    client = genai.Client(api_key=api_key)
    for _ in range(20):
        response, function_call_result_list = generate_content(client, messages, args.verbose)
        for candidate in response.candidates:
            messages.append(candidate.content)
        if not response.function_calls:
            print("Final response:")
            print(response.text)
            break
        if function_call_result_list:
            messages.append(
                types.Content(role="user", parts=function_call_result_list)
            )
        

if __name__ == "__main__":
    main()
