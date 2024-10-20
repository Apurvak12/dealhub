import React from 'react';
import Hero from './Hero';
import Searchbar from './Searchbar';
// import Image from 'next/image'; // You may want to replace this with a regular img tag.
// import { getAllProducts } from '@/lib/actions'; // Adjust the import path as needed.
import ProductCard from './ProductCard';


const getAllProducts = async () => {
  try {
    const response = await fetch('https://your-api-url.com/products'); // Replace with your actual API endpoint
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data; // Assuming the data is in the format of an array of products
  } catch (error) {
    console.error('Error fetching products:', error);
    return []; // Return an empty array in case of an error
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
      <section className="px-6 md:px-20 py-24">
        <div className="flex max-xl:flex-col gap-16">
          <div className="flex flex-col justify-center"> 
            <p className="small-text">
              Smart Shopping Starts Here:
              <img 
                src="/assets/icons/arrow-right.svg" 
                alt="arrow-right" 
                width={16} 
                height={16} 
              />
            </p>

            <h1 className="head-text">
              Unleash the Power of
              <span className="text-primary"> PriceWise</span>
            </h1>

            <p className="mt-6">
              Powerful, self-serve product and growth analytics to help you convert, engage, and retain more.
            </p>

            <Searchbar />
          </div>

          <Hero />
        </div>
      </section>

      <section className="trending-section">
        <h2 className="section-text">Trending</h2>

        <div className="flex flex-wrap gap-x-8 gap-y-16">
          {allProducts.map((product) => (
            <ProductCard key={product._id} product={product} />
          ))}
        </div>
      </section>
    </>
  );
};

export default Home;
