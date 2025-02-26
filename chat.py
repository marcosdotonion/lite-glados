import re
from llama_client import get_response
from tts import speak_threaded
from utils import (
    save_memory,
    load_memory,
    load_history,
    save_history,
    extract_think_content,
    clear_console,
)

def extract_think_content(response):
    # Debugging the raw response
    print(f"Extracting from: {response}")
    
    # Now check if there is a <think> section and extract it
    think_content = "\n".join(re.findall(r"<think>(.*?)</think>", response, re.DOTALL)).strip()
    
    # Clean response can be anything else (perhaps removing unnecessary tags)
    
    clean_response = re.sub(r"<think>.*?</think>", "", re.sub(r'\*', '', response)).strip()

    return clean_response, think_content

def chat():
    history = load_history()
    memory = load_memory()

    if "conversations" not in memory:
        memory["conversations"] = []

    print("Chat debugging started. Type 'exit' to quit.")
    clear_console()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting debug chat.")
            break

        history.append(f"User: {user_input}")
        response = get_response(user_input)

        # Debugging the raw response
        print(f"Raw response: {response}")  # Add this line to debug the full response

        clean_response, think_content = extract_think_content(response)
        history.append(f"Model: {clean_response}")
        save_history(history)

        print(f"Model: {clean_response}")
        speak_threaded(clean_response)

        if think_content.strip():
            with open("think.md", "a") as think_file:
                think_file.write(think_content + "\n")

if __name__ == "__main__":
    chat()
