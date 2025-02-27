# Lite-GLaDOS

Lite-GLaDOS is a lightweight, conversational AI modeled after GLaDOS from the *Portal* series. This project supports integration with both **llama.cpp** and **Ollama** for generating responses, allowing for flexible deployment options. 

## Features

- **Ollama Integration**: A fully functional interface with the Ollama model for fast and reliable responses.
- **llama.cpp Support**: A work-in-progress implementation of **llama.cpp**, which is a lightweight alternative for model inference. This feature is still under development.

## Installation

### Prerequisites

- Python 3.7+
- Dependencies from `requirements.txt`
- piper and piper_voices (onnx and onnx.json)

    
    pip install -r requirements.txt
    
### Running the Project

Clone the repository:

    git clone https://github.com/yourusername/lite-glados.git
    cd lite-glados

Set up your environment (optional but recommended):

    python3 -m venv myenv

### Linux/MacOS
    source myenv/bin/activate 
### Windows
    myenv\Scripts\activate.bat Windows

To run with Ollama (recommended for production):

    python3 main.py

To use llama.cpp (Work-in-progress):

Currently, llama.cpp support is a work-in-progress and may require additional setup. To run with llama.cpp:

- Ensure llama.cpp is properly set up on your system.
- Set USE_OLLAMA = False in the main.py configuration.

run:

    python3 main.py

## Configuration

USE_OLLAMA: Set this to True to use Ollama or False for llama.cpp (experimental).
OLLAMA_MODEL: Set the model name if using Ollama (e.g., glados2).
LLAMA_SERVER_URL: Set this to your local llama server URL if using llama.cpp.

## Contributing

Feel free to fork the repository, submit issues, or contribute pull requests. Contributions are always welcome!
License

This project is licensed under the MIT License - see the LICENSE file for details.


## Acknowledgments
GLaDOS from Portal for inspiration.
Llama.cpp for providing an alternative method of inference.
Ollama for providing a stable model inference environment.

If you have any questions or need help setting up Lite-GLaDOS, feel free to open an issue or contact me directly.

