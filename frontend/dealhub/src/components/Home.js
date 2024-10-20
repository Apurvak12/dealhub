import React from 'react';
import Hero from './Hero';
import Searchbar from './Searchbar';
import ProductCard from './ProductCard';
import rightarrow from '../assests/icons/arrow-right.svg'; 

const getAllProducts = async () => {
  try {
    const response = await fetch('https://your-api-url.com/products');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching products:', error);
    return [];
  }
};

const Home = () => {
  const [allProducts, setAllProducts] = React.useState([]);

  React.useEffect(() => {
    const fetchProducts = async () => {
      const products = await getAllProducts();
      setAllProducts(products);
    };

    fetchProducts();
  }, []);

  return (
    <>
      <section className="home-hero-section">
        <div className="home-hero-container">
          <div className="home-hero-content"> 
            <p className="home-subtext">
            <span>Smart Shopping Starts Here:</span>  
              <img
                src={rightarrow}
                alt="rightarrow"
                className="home-arrow-icon"
              />
            </p>

            <h1 className="home-title">
              Unleash the Power of
              <p className="home-title-highlight"> DealHUB</p>
            </h1>

            <p className="home-description">
              Powerful, self-serve product and growth analytics to help you convert, engage, and retain more.
            </p>

            <Searchbar />
          </div>

          <Hero />
        </div>
      </section>

      <section className="home-trending-section">
        <h2 className="home-section-title">Trending</h2>

        <div className="home-product-grid">
          {allProducts.map((product) => (
            <ProductCard key={product._id} product={product} />
          ))}
        </div>
      </section>
    </>
  );
};

export default Home;
