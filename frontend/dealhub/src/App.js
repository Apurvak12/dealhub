import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import Home from './components/Home';
import PriceInfoCard from './components/PriceInfoCard';
import ProductCard from './components/ProductCard';
import "./App.css";
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  

  return (
    <>
      <Navbar />
      <Home />
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

