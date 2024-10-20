import React, { useState, FormEvent } from 'react';

// Function to validate Amazon product URLs
const isValidAmazonProductURL = (url) => {
  try {
    const parsedURL = new URL(url);
    const hostname = parsedURL.hostname;

    return (
      hostname.includes('amazon.com') ||
      hostname.includes('amazon.') ||
      hostname.endsWith('amazon')
    );
  } catch (error) {
    return false;
  }
};

const Searchbar = () => {
  const [searchPrompt, setSearchPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const isValidLink = isValidAmazonProductURL(searchPrompt);

    if (!isValidLink) {
      return alert('Please provide a valid Amazon link');
    }

    try {
      setIsLoading(true);
      // Call the backend API to scrape the product
      const response = await fetch('http://your-backend-api-url/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: searchPrompt }),
      });

      if (!response.ok) {
        throw new Error('Failed to scrape product');
      }

      const data = await response.json();
      alert('Product scraped successfully!');
      console.log(data); // Handle the scraped data as needed
    } catch (error) {
      console.error(error);
      alert('An error occurred while scraping the product.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="flex flex-wrap gap-4 mt-12" onSubmit={handleSubmit}>
      <input
        type="text"
        value={searchPrompt}
        onChange={(e) => setSearchPrompt(e.target.value)}
        placeholder="Enter product link"
        className="searchbar-input"
      />

      <button
        type="submit"
        className="searchbar-btn"
        disabled={searchPrompt === ''}
      >
        {isLoading ? 'Searching...' : 'Search'}
      </button>
    </form>
  );
};

export default Searchbar;
