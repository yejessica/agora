import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def fetch_encoded_descriptions(db_path):
    """Fetch encoded descriptions and company IDs from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT company_id, encoded_description FROM companies")
    rows = cursor.fetchall()
    conn.close()

    # Deserialize JSON strings into Python lists
    encoded_data = [
        (company_id, json.loads(encoded_description))
        for company_id, encoded_description in rows
        if encoded_description is not None
    ]
    return encoded_data

def find_similar_descriptions(user_input, model, encoded_data, top_n=5):
    """Find the most similar descriptions in the database to the user input."""
    # Encode the user input
    user_embedding = model.encode(user_input)

    # Prepare data for similarity calculation
    company_ids = []
    db_embeddings = []
    for company_id, embedding in encoded_data:
        company_ids.append(company_id)
        db_embeddings.append(embedding)

    db_embeddings = np.array(db_embeddings)

    # Compute cosine similarity
    similarities = cosine_similarity([user_embedding], db_embeddings).flatten()

    # Get the top N similar entries
    top_indices = similarities.argsort()[-top_n:][::-1]
    similar_results = [(company_ids[i], similarities[i]) for i in top_indices]
    return similar_results

def fetch_company_details(db_path, company_ids):
    """Fetch company details for the top similar results."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    placeholders = ', '.join('?' for _ in company_ids)
    cursor.execute(f"SELECT company_id, name, longDescription FROM companies WHERE company_id IN ({placeholders})", company_ids)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    db_path = 'yc-companies.db'  # Update with the correct path if needed
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Fetch encoded descriptions from the database
    encoded_data = fetch_encoded_descriptions(db_path)

    # Take user input
    user_input = input("Enter a description to search for similar companies: ")

    # Find similar descriptions
    top_matches = find_similar_descriptions(user_input, model, encoded_data)

    # Fetch details for the top matches
    top_company_ids = [match[0] for match in top_matches]
    company_details = fetch_company_details(db_path, top_company_ids)

    # Display results
    print("\nTop similar companies:")
    for detail, match in zip(company_details, top_matches):
        company_id, name, description = detail
        similarity = match[1]
        print(f"Company ID: {company_id}\nName: {name}\nSimilarity: {similarity:.4f}\nDescription: {description}\n--------\n")
