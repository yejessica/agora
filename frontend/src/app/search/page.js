"use client";
import { useState } from 'react';

export default function Home() {
  const [description, setDescription] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/similar-companies', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description }),
      });

      if (!response.ok) {
        throw new Error('Error fetching similar companies');
      }

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Find Similar Companies</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="description">Enter a description:</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows="4"
          cols="50"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Searching...' : 'Submit'}
        </button>
      </form>

      <h2>Results:</h2>
      {results.length > 0 ? (
        <ul>
          {results.map((result) => (
            <li key={result.company_id}>
              <strong>{result.name}</strong> (Similarity: {result.similarity})
              <p>{result.description}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No results found yet.</p>
      )}
    </div>
  );
}
