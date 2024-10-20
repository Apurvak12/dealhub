import logo from './logo.svg';
import './App.css';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Home from './components/Home';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PriceInfoCard from './components/PriceInfoCard';
import ProductCard from './components/ProductCard';
import Searchbar from './components/Searchbar';

function App() {
  const [products, setProducts] = useState([]);
  const [priceInfo, setPriceInfo] = useState({ title: '', iconSrc: '', value: '' });

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get('/api/products'); // Fetching all products
        setProducts(response.data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };

    const fetchPriceInfo = async () => {
      try {
        const response = await axios.get('/api/price-info'); // Adjust the endpoint for price info
        setPriceInfo(response.data);
      } catch (error) {
        console.error("Error fetching price info:", error);
      }
    };

    fetchProducts();
    fetchPriceInfo();
  }, []);

  return (
    <>
      <div className="App">
        <Navbar />
        <Home />
      </div>

      <div>
        {/* Render PriceInfoCard */}
        <PriceInfoCard
          title={priceInfo.title}
          iconSrc={priceInfo.iconSrc}
          value={priceInfo.value}
        />

        {/* Render ProductCards */}
        <div className="product-list">
          {products.map((product) => (
            <ProductCard key={product._id} product={product} />
          ))}
        </div>
      </div>
    </>
  );
}

export default App;
