import openai
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os


# Loading the local variables (including the Open AI key)
load_dotenv('.env.local')


# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate embeddings using OpenAI
def get_embedding(text, model="text-embedding-ada-002"):
    client = openai.OpenAI()  # Create client instance
    response = client.embeddings.create(input=text, model=model)
    return np.array(response.data[0].embedding)

# Sample data (replace with your database information)
data = [
    {"id": 1, "description": "A cozy Italian restaurant with handmade pasta."},
    {"id": 2, "description": "A modern art museum with interactive exhibits."},
    {"id": 3, "description": "A bookstore featuring rare and antique books."},
    {"id": 4, "description": "A hiking trail with beautiful mountain views."}
]

# Convert data to a DataFrame
df = pd.DataFrame(data)

# Pre-compute embeddings for all descriptions in the database
print("Generating embeddings for database entries...")
df['embedding'] = df['description'].apply(lambda x: get_embedding(x))

# Add this helper function
def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

# Function to recommend based on user input
def recommend(user_input, top_n=3):
    # Get the embedding for the user input
    user_embedding = get_embedding(user_input)

    # Compute cosine similarity between user input and database embeddings
    df['similarity'] = df['embedding'].apply(
        lambda x: cosine_similarity(user_embedding, x)
    )

    # Sort by similarity and return top matches
    recommendations = df.sort_values(by='similarity', ascending=False).head(top_n)
    return recommendations[['id', 'description', 'similarity']]

# Example usage
if __name__ == "__main__":
    user_input = input("Enter a description of what you're looking for: ")
    results = recommend(user_input)
    print("\nTop recommendations:")
    print(results)
