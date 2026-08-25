import ollama

response = ollama.chat(
    model="qwen3:0.6b",
    messages=[
        {"role": "user", "content": "Hello! How are you?"},
    ]
)

print(response["message"]["content"])