from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the Hugging Face model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Simulated database with descriptions
database = [
    {"id": 1, "name": "Product A", "description": "This is a compact and portable gadget for everyday use."},
    {"id": 2, "name": "Product B", "description": "A durable and stylish backpack for travel and work."},
    {"id": 3, "name": "Product C", "description": "An ergonomic office chair with lumbar support."},
    {"id": 4, "name": "Product D", "description": "A high-quality wireless headphone with noise cancellation."},
]

# Precompute embeddings for the database descriptions
db_descriptions = [item['description'] for item in database]
db_embeddings = model.encode(db_descriptions)

# Function to get recommendations
def recommend(user_input, db_embeddings, database, top_n=3):
    # Encode the user input
    user_embedding = model.encode([user_input])
    
    # Compute cosine similarity between user input and database
    similarities = cosine_similarity(user_embedding, db_embeddings)
    
    # Get the indices of the top-n matches
    top_indices = np.argsort(similarities[0])[::-1][:top_n]
    
    # Retrieve the top-n items from the database
    recommendations = [database[i] for i in top_indices]
    return recommendations

# Example user input
user_description = "I need to focus with earbuds"

# Get recommendations
top_recommendations = recommend(user_description, db_embeddings, database)

# Display recommendations
print("Top Recommendations:")
for rec in top_recommendations:
    print(f"Name: {rec['name']}, Description: {rec['description']}")
