import subprocess
import requests
import re  # Import the regular expression library for cleanup

USE_OLLAMA = False # Set this to False to use llama_cpp or True to use Ollama
OLLAMA_MODEL = "glados2"
LLAMA_API_URL = "http://127.0.0.1:8080/v1"  # URL for the HTTP API for llama-based models

def clean_response_text(response_text):
    """
    Cleans the response text by removing any timestamps like "00:00:00" and instructions.
    """
    # Remove timestamps of the form "00:00:00"
    cleaned_text = re.sub(r"\d{2}:\d{2}:\d{2}", "", response_text).strip()
    
    # Remove any "Instruction" field or similar structure, if it appears in the text
    cleaned_text = re.sub(r"Instruction:.*", "", cleaned_text).strip()
    
    return cleaned_text

def get_response(prompt):
    """
    Sends a prompt to the chosen model and returns only the bot's response as a string.
    """
    try:
        if USE_OLLAMA:
            # Use Ollama through subprocess
            result = subprocess.run(
                ["ollama", "run", OLLAMA_MODEL, prompt],
                capture_output=True,
                text=True,
                check=True
            )
            # Return only the response text from Ollama
            return result.stdout.strip()

        else:
            # Use requests for HTTP API
            payload = {
                "prompt": prompt,  # Using 'prompt' instead of 'messages'
                "temperature": 0.7
            }

            # Send the request to the llama-server
            response = requests.post(LLAMA_API_URL, json=payload)

            if response.status_code == 200:
                # Print the entire response for debugging
                response_json = response.json()
                #print("Full Response JSON:", response_json)  # Debugging line
                
                # Clean the content to remove any instructions or unwanted text
                content = response_json.get('content', 'No content available')
                return clean_response_text(content)
            else:
                return f"Error: {response.status_code} - {response.text}"

    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"
