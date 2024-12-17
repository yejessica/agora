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

def find_similar_descriptions(user_input, encoded_data, top_n=9):
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

# def init_db():
#     conn = sqlite3.connect('subscriptions.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS subscriptions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             renewalDate TEXT NOT NULL,
#             price REAL NOT NULL,
#             link TEXT NOT NULL
#         )
                   
                   

#     ''')
#     conn.commit()
#     conn.close()


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
@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    """Fetch all subscription records from the database and return them as JSON."""
    connection = sqlite3.connect('subscriptions.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, name, renewalDate, price, link FROM subscriptions')
    rows = cursor.fetchall()
    connection.close()
    
    subscriptions = [
        {"id": row[0], "name": row[1], "renewalDate": row[2], "price": row[3], "link": row[4]} 
        for row in rows
    ]
    
    return jsonify(subscriptions)

@app.route('/subscriptions', methods=['POST'])
def add_subscription():
    """Insert a new subscription record into the database."""
    data = request.json
    connection = sqlite3.connect('subscriptions.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO subscriptions (name, renewalDate, price, link) 
        VALUES (?, ?, ?, ?)
    ''', (data['name'], data['renewalDate'], data['price'], data['link']))
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    
    return jsonify({
        'id': new_id,
        'name': data['name'],
        'renewalDate': data['renewalDate'],
        'price': data['price'],
        'link': data['link']
    }), 201



if __name__ == '__main__':
    app.run(debug=True)

