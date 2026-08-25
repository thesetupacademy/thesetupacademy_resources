import chromadb
import ollama
from pypdf import PdfReader

LLM_MODEL = "qwen3:0.6b"
EMBED_MODEL = "nomic-embed-text"

# 1. Load PDF
reader = PdfReader("mysql-tutorial.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text() + "\n"
    
#2. Split into chunks
chunk_size = 500

chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

#3. Creae Vector DB
client = chromadb.PersistentClient(path="the_setup_academy_db")

collection = client.get_or_create_collection(name="the_setup_academy_collection")

#4. Create embeddings and add to collection

for i,chunk in enumerate(chunks):
    embedding = ollama.embed(model=EMBED_MODEL, input=chunk)
    
    collection.add(
       ids=[str(i)],
       documents=[chunk],
       embeddings=[embedding["embeddings"][0]]
   )

print("Vector DB created and populated with embeddings.")

question = input("\nEnter your question: ")

question_embedding = ollama.embed(model=EMBED_MODEL, input=question)["embeddings"][0]

#5. Retrieve relevant chunks based on the question embedding
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)

context = "\n\n".join(results['documents'][0])

print("\nContext retrieved from the vector database:", context)

#6.Send the context LLM

prompt= f"""
Answer the question based on the context below.

Context:
{context}

Question: {question}
"""

print('\nPrompt sent to LLM:', prompt)

response = ollama.chat(LLM_MODEL, messages=[{"role": "user", "content": prompt}])

print("\nAnswer:")
print(response["message"]["content"])

    
    