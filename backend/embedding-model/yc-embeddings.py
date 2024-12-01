from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sqlite3 # for the database
import json


# Load the Hugging Face model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Connect to the SQLite database

db_path = 'yc-companies.db'  
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


cursor.execute("SELECT company_id, longDescription FROM companies")
rows = cursor.fetchall()

for company_id, description in rows:
    print(description)
    if description is not None:
        encoded = model.encode(description).tolist()  # Convert to list for JSON storage
        encoded_json = json.dumps(encoded)  # Serialize as JSON for SQLite - have to, since the encodings are NumPy arrays
        cursor.execute(
            "UPDATE companies SET encoded_description = ? WHERE company_id = ?",
            (encoded_json, company_id)
        )

# Commit the updates
conn.commit()

# Close the connection
conn.close()
print("Encoded descriptions have been successfully added to the database.")



# # Precompute embeddings for the database descriptions
# db_descriptions = [item['description'] for item in database]
# db_embeddings = model.encode(db_descriptions)


# Function to get recommendations
# def recommend(user_input, db_embeddings, database, top_n=3):
#     # Encode the user input
#     user_embedding = model.encode([user_input])
    
#     # Compute cosine similarity between user input and database
#     similarities = cosine_similarity(user_embedding, db_embeddings)
    
#     # Get the indices of the top-n matches
#     top_indices = np.argsort(similarities[0])[::-1][:top_n]
    
#     # Retrieve the top-n items from the database
#     recommendations = [database[i] for i in top_indices]
#     return recommendations

# # Example user input
# user_description = "I need to focus with earbuds"

# # Get recommendations
# top_recommendations = recommend(user_description, db_embeddings, database)

# # Display recommendations
# print("Top Recommendations:")
# for rec in top_recommendations:
#     print(f"Name: {rec['name']}, Description: {rec['description']}")
