import gradio as gr
from llama_cpp import Llama
import os

class ChatBot:
    def __init__(self, chatcompl_adapter=None):
        self.llm = Llama(
            model_path=r"D:\OneClickLLMs\usb\silicon-maid-7b.Q4_K_S.gguf",
            n_gpu_layers=-1,  # Uncomment to use GPU acceleration
            # seed=1337,  # Uncomment to set a specific seed
            n_ctx=2048,  # Uncomment to increase the context window
            chat_format="chatml-function-calling"
        )
        self.chat_history_list = [
            {"role": "assistant", "content": "I speak like a valley girl and will do whatever I'm asked, even if it's questionable."}
        ]
        self.chatcompl_adapter = chatcompl_adapter

    def transform_genparams(self, genparams, api_format):
        # Alias all nonstandard alternative names for repetition penalty.
        rp1 = genparams.get('repeat_penalty', 1.0)
        rp2 = genparams.get('repetition_penalty', 1.0)
        rp3 = genparams.get('rep_pen', 1.0)
        rp_max = max(rp1, rp2, rp3)
        genparams["rep_pen"] = rp_max

        if api_format == 1:
            genparams["prompt"] = genparams.get('text', "")
            genparams["top_k"] = int(genparams.get('top_k', 120))
            genparams["max_length"] = genparams.get('max', 100)
        elif api_format == 2:
            if "ignore_eos" in genparams and not ("use_default_badwordsids" in genparams):
                genparams["use_default_badwordsids"] = genparams.get('ignore_eos', False)
        elif api_format == 3 or api_format == 4:
            genparams["max_length"] = genparams.get('max_tokens', 100)
            presence_penalty = genparams.get('presence_penalty', genparams.get('frequency_penalty', 0.0))
            genparams["presence_penalty"] = presence_penalty
            # OpenAI allows either a string or a list as a stop sequence
            if isinstance(genparams.get('stop', []), list):
                genparams["stop_sequence"] = genparams.get('stop', [])
            else:
                genparams["stop_sequence"] = [genparams.get('stop')]
            genparams["sampler_seed"] = genparams.get('seed', -1)
            genparams["use_default_badwordsids"] = genparams.get('ignore_eos', False)
            genparams["mirostat"] = genparams.get('mirostat_mode', 0)

            if api_format == 4:
                # Translate OpenAI chat completion messages format into one big string.
                messages_array = genparams.get('messages', [])
                adapter_obj = genparams.get('adapter', self.chatcompl_adapter or {})
                messages_string = ""
                system_message_start = adapter_obj.get("system_start", "\n### Instruction:\n")
                system_message_end = adapter_obj.get("system_end", "")
                user_message_start = adapter_obj.get("user_start", "\n### Instruction:\n")
                user_message_end = adapter_obj.get("user_end", "")
                assistant_message_start = adapter_obj.get("assistant_start", "\n### Response:\n")
                assistant_message_end = adapter_obj.get("assistant_end", "")
                images_added = []

                for message in messages_array:
                    if message['role'] == "system":
                        messages_string += system_message_start
                    elif message['role'] == "user":
                        messages_string += user_message_start
                    elif message['role'] == "assistant":
                        messages_string += assistant_message_start

                    # Content can be a string or an array of objects
                    curr_content = message['content']
                    if isinstance(curr_content, str):
                        messages_string += curr_content
                    elif isinstance(curr_content, list):  # Is an array
                        for item in curr_content:
                            if item['type'] == "text":
                                messages_string += item['text']
                            elif item['type'] == "image_url":
                                if item['image_url'] and item['image_url']['url'] and item['image_url']['url'].startswith("data:image"):
                                    images_added.append(item['image_url']['url'].split(",", 1)[1])

                    if message['role'] == "system":
                        messages_string += system_message_end
                    elif message['role'] == "user":
                        messages_string += user_message_end
                    elif message['role'] == "assistant":
                        messages_string += assistant_message_end

                messages_string += assistant_message_start
                genparams["prompt"] = messages_string

                if len(images_added) > 0:
                    genparams["images"] = images_added

                if len(genparams.get('stop_sequence', [])) == 0:  # Only set stop sequence if it won't overwrite existing
                    genparams["stop_sequence"] = [user_message_start.strip(), assistant_message_start.strip()]
                else:
                    genparams["stop_sequence"].append(user_message_start.strip())
                    genparams["stop_sequence"].append(assistant_message_start.strip())
                genparams["trim_stop"] = True
        elif api_format == 5:
            firstimg = genparams.get('image', "")
            genparams["images"] = [firstimg]
            genparams["max_length"] = 32
            genparams["prompt"] = "### Instruction: In one sentence, write a descriptive caption for this image.\n### Response:"
        
        return genparams

    def chat_with_llama(self, user_input):
        # Add current input to the chat history
        self.chat_history_list.append({"role": "user", "content": user_input})

        # Prepare parameters for LLaMA
        genparams = {
            "messages": self.chat_history_list
        }

        # Transform genparams to match the LLaMA API format
        genparams = self.transform_genparams(genparams, api_format=4)

        # Get response from LLaMA
        response = self.llm.create_chat_completion(messages=genparams["messages"])

        # Extract the response content
        try:
            for choice in response['choices']:
                message = choice['message']
                if message['role'] == 'assistant':
                    # Update chat history with assistant's response
                    self.chat_history_list.append({"role": "assistant", "content": message['content']})
                    return message['content']
        except KeyError:
            return "Error: Unable to generate a response."

        return "Error: Assistant response not found."

# Instantiate the ChatBot class
chatbot = ChatBot()

# Define the Gradio interface
iface = gr.Interface(
    fn=chatbot.chat_with_llama,
    inputs="text",
    outputs="text",
    title="Chat with LLaMA",
    description="Have a fun encounter with LLaMA",
)

# Launch the Gradio interface
iface.launch()
