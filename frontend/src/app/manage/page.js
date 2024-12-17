"use client";

import { useState, useEffect } from 'react';

export default function SubscriptionsPage() {
  const [subscriptions, setSubscriptions] = useState([]);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    renewalDate: '',
    price: '',
    link: ''
  });

  useEffect(() => {
    const fetchSubscriptions = async () => {
      try {
        const response = await fetch('http://localhost:5000/subscriptions');
        const data = await response.json();
        setSubscriptions(data);
      } catch (error) {
        console.error('Error fetching subscriptions:', error);
      }
    };
    
    fetchSubscriptions();
  }, []);

  const openPopup = () => setIsPopupOpen(true);
  const closePopup = () => setIsPopupOpen(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const response = await fetch('http://localhost:5000/subscriptions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      const newSubscription = await response.json();
      setSubscriptions([...subscriptions, newSubscription]);
      setFormData({ name: '', renewalDate: '', price: '', link: '' });
      closePopup();
    } else {
      console.error('Failed to save subscription');
    }
  };

  return (
    <div className="p-8 bg-gray-100 min-h-screen font-helvetica">
      <h1 className="text-3xl font-bold text-center text-[#7456A5] mb-6">Subscription Tracker</h1>
      <button 
        onClick={openPopup} 
        className="bg-[#7456A5] text-white px-6 py-3 rounded-lg hover:bg-[#7456A5] transition-all shadow-md"
      >
        + Add Subscription
      </button>
      
      {isPopupOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
        <div className="bg-white p-10 rounded-lg shadow-xl w-96">
          <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Add New Subscription</h2>
          <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-semibold mb-2" htmlFor="name">Subscription Name</label>
                <input 
                  type="text" 
                  id="name" 
                  name="name" 
                  value={formData.name} 
                  onChange={handleInputChange} 
                  className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#7456A5]" 
                  required 
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-semibold mb-2" htmlFor="renewalDate">Renewal Date</label>
                <input 
                  type="date" 
                  id="renewalDate" 
                  name="renewalDate" 
                  value={formData.renewalDate} 
                  onChange={handleInputChange} 
                  className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#7456A5]" 
                  required 
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-semibold mb-2" htmlFor="price">Price</label>
                <input 
                  type="number" 
                  id="price" 
                  name="price" 
                  value={formData.price} 
                  onChange={handleInputChange} 
                  className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#7456A5]" 
                  required 
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-semibold mb-2" htmlFor="link">Link to Website</label>
                <input 
                  type="url" 
                  id="link" 
                  name="link" 
                  value={formData.link} 
                  onChange={handleInputChange} 
                  className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#7456A5]" 
                  required 
                />
              </div>

              <div className="flex justify-end">
                <button 
                  type="button" 
                  onClick={closePopup} 
                  className="bg-gray-400 text-white px-4 py-2 rounded-lg mr-2 hover:bg-gray-500 transition-all"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="bg-[#7456A5] text-white px-4 py-2 rounded-lg hover:bg-[#7456A5] transition-all shadow-md"
                >
                  Add
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <h2 className="text-2xl font-bold mt-10 mb-6 text-[#7456A5]">All Subscriptions</h2>
      <table className="w-full border-collapse bg-white shadow-lg rounded-lg overflow-hidden">
        <thead>
          <tr className="bg-[#7456A5] text-white">
            <th className="p-4 text-left">Name</th>
            <th className="p-4 text-left">Renewal Date</th>
            <th className="p-4 text-left">Price</th>
            <th className="p-4 text-left">Website</th>
          </tr>
        </thead>
        <tbody>
          {subscriptions.map((sub, index) => (
            <tr key={index} className="border-t border-gray-100 hover:bg-gray-50 transition-all">
              <td className="p-4">{sub.name}</td>
              <td className="p-4">{sub.renewalDate}</td>
              <td className="p-4">${sub.price}</td>
              <td className="p-4">
                <a 
                  href={sub.link} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="text-[#7456A5] hover:underline"
                >
                  Visit Site
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
