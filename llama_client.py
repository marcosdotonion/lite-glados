import subprocess
import requests

USE_OLLAMA = True  # Set this to False to use llama-server or True to use Ollama
OLLAMA_MODEL = "glados2"
LLAMA_SERVER_URL = "http://127.0.0.1:8080"  # URL for llama-server

def get_response(prompt):
    """
    Sends a prompt to the chosen model (Ollama, llama-server) and returns only the bot's response.
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
        
        elif LLAMA_SERVER_URL:  # If we're using llama-server
            # Send the prompt to llama-server using a POST request
            response = requests.post(
                f"{LLAMA_SERVER_URL}/completions",
                json={
                    "prompt": prompt,
                    "max_tokens": 100,  # You can adjust these parameters
                    "top_k": 20,
                    "top_p": 0.85,
                    "temperature": 0.2,
                    "frequency_penalty": 0.7,  # Penalizes frequent tokens more
                    "presence_penalty": 0.3  # Low presence penalty to reduce introduction of irrelevant information
                },
                headers={"Accept": "application/json"}  # Ensure we request JSON response
            )
            
            # Check if the response is successful
            if response.status_code == 200:
                # Return the raw JSON response from llama-server
                return response.json()  # This returns the entire JSON response from the server
            else:
                return f"Error: Received status code {response.status_code}"

        else:
            return "Error: No model system selected."

    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

