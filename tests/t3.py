from llama_cpp import Llama

# Initialize the model
llm = Llama(model_path="/usr/share/ollama/.ollama/models/TinySwallow-1.5B.Q4_K_M.gguf", chat_format="chatml")

# Create chat completion
response = llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that outputs in JSON.",
        },
        {"role": "user", "content": "Who won the world series in 2020"},
    ],
    response_format={
        "type": "json_object",
    },
    temperature=0.7,
)

# Print the result
print(response)
