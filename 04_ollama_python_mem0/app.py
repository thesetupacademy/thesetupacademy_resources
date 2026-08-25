import ollama
from mem0 import Memory


#configuration
config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "qwen3:0.6b",
            "ollama_base_url": "http://localhost:11434"
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "my_memories_training",
            "path": "./qdrant_db",
            "embedding_model_dims": 768
        }
    }
}

#memory initialization
memory = Memory.from_config(config)

user_id = "user_the_setup_academy"

memory.add('My Channel Name is The Setup Academy', user_id=user_id)

#memory search
memory_text = memory.search('What is my channel name?', filters={"user_id": user_id})

memory_text = memory_text["results"][0]["memory"] if memory_text["results"] else "No memory found."

#interacting with the model
response = ollama.chat(
    model="qwen3:0.6b",
    messages=[
        {"role": "user", "content": f"My memory is: {memory_text}. Can you help me with this information?"}
    ]
)

result = response["message"]["content"]

print('Response from the model:', result)


