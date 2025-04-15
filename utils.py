import json
import os
import re

def clear_console():
    # Code to clear the console, e.g., for UNIX-based systems
    print("\033c", end="")

def load_memory():
    """
    Loads memory from memory.json.
    """
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            return json.load(f)
    return {"conversations": [], "personality": "inate"}

def save_memory(memory):
    """
    Saves memory to memory.json.
    """
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)

def load_history():
    """
    Loads conversation history.
    """
    if os.path.exists("output.md"):
        with open("output.md", "r") as f:
            return f.readlines()
    return []

def save_history(history):
    """
    Saves conversation history to output.md.
    """
    with open("output.md", "a") as f:
        f.writelines(history)

import re

def extract_think_content(response):
    if isinstance(response, str):
        # If the response is a string, you can search for <think> tags or handle it as needed
        think_content = "\n".join(re.findall(r"<think>(.*?)</think>", response, re.DOTALL)).strip()
        clean_response = response.strip()  # Or whatever else you want to clean the response
        return clean_response, think_content
    else:
        # Handle case where the response is a dictionary, if applicable
        content = response.get("content", "")
        think_content = "\n".join(re.findall(r"<think>(.*?)</think>", content, re.DOTALL)).strip()
        clean_response = content.strip()  # Or whatever else you want to clean the response
        return clean_response, think_content


