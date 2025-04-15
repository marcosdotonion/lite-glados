import requests

url = "http://127.0.0.1:8080/completion"
prompt = "Building a website can be done in 10 simple steps:"

payload = {
    "prompt": prompt,
    "n_predict": 64,
    "stream": False
    
}

response = requests.post(url, json=payload)
print(response.json().get("content", "No response"))
