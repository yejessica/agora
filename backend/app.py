from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Load the SentenceTransformer model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Database path
DB_PATH = 'embedding-model/yc-companies.db'

# In-memory cache to store the encoded descriptions
encoded_data_cache = None

def fetch_encoded_descriptions():
    """Fetch encoded descriptions and company IDs from the database."""
    global encoded_data_cache
    if encoded_data_cache is not None:
        return encoded_data_cache

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT company_id, encoded_description FROM companies")
    rows = cursor.fetchall()
    conn.close()

    # Deserialize JSON strings into Python lists
    encoded_data_cache = [
        (company_id, json.loads(encoded_description))
        for company_id, encoded_description in rows
        if encoded_description is not None
    ]
    return encoded_data_cache

def find_similar_descriptions(user_input, encoded_data, top_n=5):
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

def fetch_company_details(company_ids):
    """Fetch company details for the top similar results."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    placeholders = ', '.join('?' for _ in company_ids)
    cursor.execute(f"SELECT company_id, name, longDescription FROM companies WHERE company_id IN ({placeholders})", company_ids)
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/api/similar-companies', methods=['POST'])
def get_similar_companies():
    data = request.json
    user_input = data.get('description', '')

    if not user_input:
        return jsonify({'error': 'Description is required'}), 400

    # Fetch encoded descriptions and find similar companies
    encoded_data = fetch_encoded_descriptions()
    top_matches = find_similar_descriptions(user_input, encoded_data)

    # Fetch company details
    top_company_ids = [match[0] for match in top_matches]
    company_details = fetch_company_details(top_company_ids)

    # Format the response
    results = []
    for detail, match in zip(company_details, top_matches):
        company_id, name, description = detail
        similarity = match[1]
        results.append({
            'company_id': company_id,
            'name': name,
            'description': description,
            'similarity': round(similarity, 4),
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
