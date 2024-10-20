import logo from './logo.svg';
import './App.css';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Home from './components/Home';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PriceInfoCard from './components/PriceInfoCard';
import ProductCard from './components/ProductCard';

function App() {


  const App = () => {
    const [products, setProducts] = useState([]);
    const [priceInfo, setPriceInfo] = useState({ title: '', iconSrc: '', value: '' });
  
    useEffect(() => {
      const fetchProducts = async () => {
        const response = await axios.get('/api/products'); // Adjust the endpoint as needed
        setProducts(response.data);
      };
  
      const fetchPriceInfo = async () => {
        const response = await axios.get('/api/price-info'); // Adjust the endpoint for price info
        setPriceInfo(response.data);
      };
  
      fetchProducts();
      fetchPriceInfo();
    }, []);
  
  
  return (<>
    <div className="App">
       <Navbar/>
       <Home/>
       <Hero/>
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
}

export default App;
