import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the Chroma client and collection
persist_directory = "./memory_db"

client = chromadb.PersistentClient(path=persist_directory)
collection = client.get_or_create_collection("memory_collection")

# Initialize the SentenceTransformer model for embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

def add_memory(user_input, response):
    # Embed the user input and response
    user_input_embed = model.encode([user_input])[0]
    response_embed = model.encode([response])[0]

    # Log embeddings and inputs
    #print(f"User Input Embedding: {user_input_embed}")
    #print(f"Response Embedding: {response_embed}")
    
    # Add the memory to ChromaDB
    collection.add(
        documents=[user_input, response],  # Store the user input and the response
        embeddings=[user_input_embed, response_embed],  # Store embeddings
        metadatas=[{"type": "user_input"}, {"type": "response"}],  # Metadata
        ids=[str(hash(user_input)), str(hash(response))]  # Unique IDs
    )
    #print(f"Memory added: {user_input} -> {response}")

    
    # Debugging: Print what is being added
    #print(f"Added memory: {user_input} -> {response}")


def get_relevant_memory(query):
    """
    Retrieves the most relevant memory from ChromaDB based on the query.
    """
    query_embed = model.encode([query])[0]

    # Log query embedding
    #print(f"Query embedding: {query_embed}")

    # Search for the most relevant memory
    results = collection.query(
        query_embeddings=[query_embed],
        n_results=1  # Get the top 1 result
    )
    
    # Debugging: Print results to see what we're retrieving
    #print(f"Query results: {results}")

    # Check if any results are found
    if results['documents']:
        return results['documents'][0]  # Return the most relevant document
    else:
        return None



def list_all_memories():
    """
    Lists all the memories stored in ChromaDB.
    """
    # Get all documents stored in the ChromaDB collection
    all_documents = collection.get()

    if all_documents and 'documents' in all_documents:
        for i, doc in enumerate(all_documents['documents']):
            print(f"/// MEMORY {i + 1} /// {doc}")
    else:
        print("No memories found.")
