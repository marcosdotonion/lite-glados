Lite-GLaDOS

Lite-GLaDOS is a lightweight, conversational AI modeled after GLaDOS from the Portal series. This project supports integration with both llama.cpp and Ollama for generating responses, allowing for flexible deployment options.
Requirements

    Python 3.7+

    Dependencies from requirements.txt

    piper and piper_voices (including onnx and onnx.json)

Installation

    Clone the repository:

git clone https://github.com/yourusername/lite-glados.git
cd lite-glados

(Optional) Set up a Python virtual environment:

python3 -m venv myenv
source myenv/bin/activate  # Linux/MacOS
myenv\Scripts\activate.bat # Windows

Install dependencies:

    pip install -r requirements.txt

Usage
Run with Ollama (recommended for production):

python3 main.py

Run with llama.cpp (Work-in-progress):

    Make sure you have llama.cpp set up correctly on your system.

    Edit main.py to set USE_OLLAMA = False.

    Optionally, configure LLAMA_SERVER_URL to point to your local llama server.

python3 main.py

Configuration

    USE_OLLAMA: Set to True to use Ollama or False to use llama.cpp (experimental).

    OLLAMA_MODEL: The Ollama model name to use (e.g., glados2).

    LLAMA_SERVER_URL: URL of your local llama.cpp inference server.

Contributing

Feel free to fork the repository, submit issues, or contribute pull requests. Contributions are always welcome!
License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    GLaDOS from Portal for inspiration.

    Llama.cpp for providing an alternative lightweight inference method.

    Ollama for providing a stable model inference environment.
