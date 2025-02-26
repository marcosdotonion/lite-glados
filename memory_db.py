import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the Chroma client and collection
client = chromadb.Client()
collection = client.create_collection("memory_collection")

# Initialize the SentenceTransformer model for embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

def add_memory(user_input, response):
    """
    Adds memory to ChromaDB.
    Embeds the user input and response using sentence-transformers.
    """
    # Embed the user input and response
    user_input_embed = model.encode([user_input])[0]
    response_embed = model.encode([response])[0]

    # Add the memory to the ChromaDB collection
    collection.add(
        documents=[user_input, response],
        embeddings=[user_input_embed, response_embed],
        metadatas=[{"type": "user_input"}, {"type": "response"}],
        ids=[str(hash(user_input)), str(hash(response))]  # Unique IDs
    )

def get_relevant_memory(query):
    """
    Retrieves the most relevant memory from ChromaDB based on the query.
    """
    query_embed = model.encode([query])[0]

    # Search for the most relevant memory
    results = collection.query(
        query_embeddings=[query_embed],
        n_results=1  # Get the top 1 result
    )

    # Check if any results are found
    if results['documents']:
        return results['documents'][0]  # Return the most relevant document
    else:
        return None
