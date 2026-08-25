import chromadb

client = chromadb.PersistentClient(path="./the_setup_academy_db")


collection = client.get_or_create_collection("the_setup_academy_docs")

print("Collection created or retrieved successfully.")

collection.delete(ids=["doc1", "doc2", "doc3"])  # Clear the collection before adding new documents

collection.add(
    ids=["doc1", "doc2", "doc3"],
    documents=["This is the first document.", "This is the second document.", "This is the third document."]
)

print("Documents added to the collection.")

results = collection.query(
    query_texts=["enjoy learning"], 
    n_results=1
)


print("Query results:")
for doc in results['documents'][0]:
    print(f"Doc: {doc}")
    