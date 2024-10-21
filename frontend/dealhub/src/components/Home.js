import React, { useState } from 'react';
import Hero from './Hero';
import Searchbar from './Searchbar';
import ProductCard from './ProductCard';
import rightarrow from '../assests/icons/arrow-right.svg';

const Home = () => {
  const [url, setUrl] = useState(''); 

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/fetch', { // Adjust to your actual API URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch product info');
      }

      const result = await response.json();
      console.log(result); // Check the result from the API

      // reroute to the product page
      // results["title"]
      // method ( http://localhost:5000/fetchs ) tyacht title pass karu
      const details = await fetch('http://localhost:5000/fetchs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: result.title }),

      });
      if(!details.ok){
        throw new Error('Failed to fetch product details');
      }
      const productDetails = await details.json();
      console.log(productDetails);
      
    } catch (error) {
      console.error('Error submitting URL:', error);
    }
  };

  return (
    <>
      <section className="home-hero-section">
        <div className="home-hero-container">
          <div className="home-hero-content"> 
            <p className="home-subtext">
              <span>Smart Shopping Starts Here:</span>  
              <img src={rightarrow} alt="rightarrow" className="home-arrow-icon" />
            </p>

            <h1 className="home-title">
              Unleash the Power of
              <p className="home-title-highlight"> DealHUB</p>
            </h1>

            <p className="home-description">
              Powerful, self-serve product and growth analytics to help you convert, engage, and retain more.
            </p>

            <form onSubmit={handleSubmit}>
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Enter product URL"
                required
              />
              <button type="submit">Submit</button>
            </form>
          </div>

          <Hero />
        </div>
      </section>
    </>
  );
};

export default Home;