from memory_db import add_memory, get_relevant_memory
from utils import extract_think_content
from personality import get_personality_prompt
from llama_client import get_response
from tts import speak_threaded

def main():
    print("GLaDOS Candy. For fuck sakes.")
    speak_threaded("Oh [[no]]. Not [[again.]]", speed=0.1)

    while True:
        user_input = input("command-line: ")

        if user_input.lower() == "exit":
            speak_threaded("See ya!")
            break

        # Check if a relevant memory exists
        relevant_memory = get_relevant_memory(user_input)
        if relevant_memory:
            user_input = f"{relevant_memory}\n\n{user_input}"  # Append memory context

        # Generate personality-based prompt
        prompt = get_personality_prompt({}, user_input)
        response = get_response(prompt)

        # Process response
        clean_response, think_content = extract_think_content(response)
        speak_threaded(clean_response)
        print(clean_response)

        # Store the conversation in ChromaDB
        add_memory(user_input, clean_response)

if __name__ == "__main__":
    main()
