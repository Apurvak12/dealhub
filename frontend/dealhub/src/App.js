import React from 'react';
import { Route, Routes } from 'react-router-dom';
import axios from 'axios';
import Navbar from './components/Navbar';
import Home from './components/Home';
import PriceInfoCard from './components/PriceInfoCard';
import ProductCard from './components/ProductCard';
import Page from '../src/products/[id]/page'; // Ensure this path is correct
import "./App.css";
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <>
      <Navbar />
       <Routes>
        <Route path="/" element={<Home />} /> 
         <Route path="/products/:title" element={<Page />} /> 
       </Routes> 
      {/* Uncomment if you want to include PriceInfoCard and ProductCard outside the routes */}
      {/* <PriceInfoCard
        title={priceInfo.title}
        iconSrc={priceInfo.iconSrc}
        value={priceInfo.value}
      />
      <div className="product-list">
        {products.map((product) => (
          <ProductCard key={product._id} product={product} />
        ))}
      </div> */}
    </>
  );
}

export default App;
