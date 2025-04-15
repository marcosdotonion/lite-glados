from memory_db import add_memory, get_relevant_memory, list_all_memories
from utils import extract_think_content
from personality import get_personality_prompt
from llama_client import get_response
from tts import speak_threaded

def main():
    print("GLaDOS Candy. For fuck sakes.")
    #speak_threaded("Oh [[no]]. Not [[again.]]", speed=0.1)
    speak_threaded("You will suffer.", speed=0.1)

    previous_input = ""

    while True:
        user_input = input("command-line: ")

        if user_input.lower() == "exit":
            speak_threaded("See ya!")
            break

        if user_input.lower() == "/memory":
            print("Listing all memories stored in ChromaDB:")
            list_all_memories()
            continue

        relevant_memory = get_relevant_memory(user_input)
        if relevant_memory and relevant_memory != previous_input:
            user_input = f"{relevant_memory}\n\n{user_input}"  # Append only if relevant

        # Generate personality-based prompt
        prompt = get_personality_prompt({}, user_input)
        response = get_response(prompt)
        #print("Raw response:", response)  # Debugging line
        
        clean_response, think_content = extract_think_content(response)
        #print("Clean response:", clean_response)  # Debugging line


        if not clean_response:
            clean_response = "No response generated."

        speak_threaded(clean_response)
        print(clean_response)

        add_memory(user_input, clean_response)
        previous_input = user_input  # Store the current input to avoid appending again
        #print(f"MEMORY ADDED: {user_input} -> {clean_response}")

if __name__ == "__main__":
    main()
