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
    <div className="flex items-center justify-center min-h-screen bg-gray-100 font-helvetica">
      <div className="w-[70%] h-auto text-center p-16 rounded-3xl">
        <h1 className="text-[#7456A5] text-center font-helvetica text-[48px] font-semibold leading-none mb-8">Agora</h1>
        <p className='mb-5'>Search for similar companies that meet your business needs.</p>
        {/* <form onSubmit={handleSubmit}>
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
        </form> */}



        <form className="max-w-md mx-auto mb-8" onSubmit={handleSubmit}>   
            <label htmlFor="default-search" className="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
            <div className="relative">
                <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                    <svg className="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                        <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                    </svg>
                </div>
                <input type="search" id="default-search description" value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:[#7456A5] focus:[#7456A5] dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search through different companies..." required />
                <button type="submit" className="text-white absolute end-2.5 bottom-2.5 bg-[#7456A5] hover:bg-[#503876] focus:ring-4 focus:outline-none focus:[#7456A5] font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" disabled={loading}>{loading ? 'Searching...' : 'Search'}</button>
            </div>
        </form>


        {/* <h2>Results:</h2>
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
        )} */}

        {results.length > 0 && (
          <>
            <h2 className='text-[#3e2763] text-center font-helvetica text-[24px] font-semibold leading-none mb-3'>Similar Companies</h2>
            {/* <h2>Results:</h2> */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {results.map((result) => (
                <div 
                  key={result.company_id} 
                  className="bg-white shadow-md rounded-lg p-6 border border-gray-200"
                >
                  <h3 className="text-xl font-bold mb-2">{result.name}</h3>
                  {/* <p className="text-sm text-gray-500 mb-4">Similarity: {result.similarity}</p> */}
                  <p className="text-gray-700">{result.description}</p>
                </div>
              ))}
            </div>
          </>
        )}

        </div>
      
    </div>
  );
}
