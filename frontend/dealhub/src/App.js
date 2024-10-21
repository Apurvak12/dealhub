import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import Home from './components/Home';
import PriceInfoCard from './components/PriceInfoCard';
import ProductCard from './components/ProductCard';
import "./App.css";

function App() {
  const [products, setProducts] = useState([]);
  const [priceInfo, setPriceInfo] = useState({ title: '', iconSrc: '', value: '' });

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get('/api/products');
        setProducts(response.data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };

    fetchProducts();
  }, []);

  return (
    <>
      <Navbar />
      <Home />
      <PriceInfoCard
        title={priceInfo.title}
        iconSrc={priceInfo.iconSrc}
        value={priceInfo.value}
      />
      <div className="product-list">
        {products.map((product) => (
          <ProductCard key={product._id} product={product} />
        ))}
      </div>
    </>
  );
}

export default App;

