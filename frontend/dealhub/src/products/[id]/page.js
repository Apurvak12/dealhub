import React, { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom"; // Change useHistory to useNavigate
import Modal from '../../components/Modal';
import PriceInfoCard from "../../components/PriceInfoCard";
import ProductCard from "../../components/ProductCard";

// Fetch product details by title
const fetchProductByTitle = async (title) => {
  try {
    const res = await fetch(`http://localhost:5000/fetchs`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title }), // Send the title in the request body
    });

    if (!res.ok) throw new Error("Failed to fetch product");
    return await res.json();
  } catch (error) {
    console.error("Error fetching product by title:", error);
    return null;
  }
};

// Fetch similar products based on product ID
const fetchSimilarProducts = async (id) => {
  try {
    const res = await fetch(`http://localhost:5000/products/${id}/similar`);
    if (!res.ok) throw new Error("Failed to fetch similar products");
    return await res.json();
  } catch (error) {
    console.error("Error fetching similar products:", error);
    return [];
  }
};

const ProductDetails = () => {
  const { title } = useParams(); // Get the product title from URL parameters
  const navigate = useNavigate(); // Change to useNavigate
  const [product, setProduct] = useState(null);
  const [similarProducts, setSimilarProducts] = useState([]);

  useEffect(() => {
    const fetchProductData = async () => {
      const productData = await fetchProductByTitle(title);
      if (!productData) {
        navigate("/"); // Redirect to home page if product not found
      } else {
        setProduct(productData);
        
        // Fetch similar products based on the product ID
        const similarProductsData = await fetchSimilarProducts(productData._id); // Use _id instead of id
        setSimilarProducts(similarProductsData);
      }
    };

    fetchProductData();
  }, [title, navigate]);

  if (!product) return <div>Loading...</div>;

  return (
    <div className="product-container">
      <div className="flex gap-28 xl:flex-row flex-col">
        <div className="product-image">
          <img
            src={product.image}
            alt={product.title}
            width={580}
            height={400}
            className="mx-auto"
          />
        </div>

        <div className="flex-1 flex flex-col">
          <div className="flex justify-between items-start gap-5 flex-wrap pb-6">
            <div className="flex flex-col gap-3">
              <p className="text-[28px] text-secondary font-semibold">
                {product.title}
              </p>

              <a
                href={product.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-base text-black opacity-50"
              >
                Visit Product
              </a>
            </div>

            <div className="flex items-center gap-3">
              <div className="product-hearts">
                <img src="/assets/icons/red-heart.svg" alt="heart" width={20} height={20} />
                <p className="text-base font-semibold text-[#D46F77]">
                  {product.reviewsCount}
                </p>
              </div>

              <div className="p-2 bg-white-200 rounded-10">
                <img src="/assets/icons/bookmark.svg" alt="bookmark" width={20} height={20} />
              </div>

              <div className="p-2 bg-white-200 rounded-10">
                <img src="/assets/icons/share.svg" alt="share" width={20} height={20} />
              </div>
            </div>
          </div>

          <div className="product-info">
            <div className="flex flex-col gap-2">
              <p className="text-[34px] text-secondary font-bold">
                {product.currency} {product.currentPrice?.toFixed(2)}
              </p>
              <p className="text-[21px] text-black opacity-50 line-through">
                {product.currency} {product.originalPrice?.toFixed(2)}
              </p>
            </div>

            <div className="flex flex-col gap-4">
              <div className="flex gap-3">
                <div className="product-stars">
                  <img src="/assets/icons/star.svg" alt="star" width={16} height={16} />
                  <p className="text-sm text-primary-orange font-semibold">
                    {product.stars || "25"}
                  </p>
                </div>

                <div className="product-reviews">
                  <img src="/assets/icons/comment.svg" alt="comment" width={16} height={16} />
                  <p className="text-sm text-secondary font-semibold">
                    {product.reviewsCount} Reviews
                  </p>
                </div>
              </div>

              <p className="text-sm text-black opacity-50">
                <span className="text-primary-green font-semibold">93% </span> of buyers have
                recommended this.
              </p>
            </div>
          </div>

          <div className="my-7 flex flex-col gap-5">
            <div className="flex gap-5 flex-wrap">
              <PriceInfoCard
                title="Current Price"
                iconSrc="/assets/icons/price-tag.svg"
                value={`${product.currency} ${product.currentPrice?.toFixed(2)}`}
              />
              <PriceInfoCard
                title="Average Price"
                iconSrc="/assets/icons/chart.svg"
                value={`${product.currency} ${product.averagePrice?.toFixed(2)}`} // Ensure averagePrice is available
              />
              <PriceInfoCard
                title="Highest Price"
                iconSrc="/assets/icons/arrow-up.svg"
                value={`${product.currency} ${product.highestPrice?.toFixed(2)}`} // Ensure highestPrice is available
              />
              <PriceInfoCard
                title="Lowest Price"
                iconSrc="/assets/icons/arrow-down.svg"
                value={`${product.currency} ${product.lowestPrice?.toFixed(2)}`} // Ensure lowestPrice is available
              />
            </div>
          </div>

          <Modal productId={product._id} />
        </div>
      </div>

      <div className="flex flex-col gap-16">
        <div className="flex flex-col gap-5">
          <h3 className="text-2xl text-secondary font-semibold">Product Description</h3>
          <div className="flex flex-col gap-4">
            {product.description?.split("\n").map((line, index) => (
              <p key={index}>{line}</p>
            ))}
          </div>
        </div>

        <button className="btn w-fit mx-auto flex items-center justify-center gap-3 min-w-[200px]">
          <img src="/assets/icons/bag.svg" alt="check" width={22} height={22} />
          <Link to="/" className="text-base text-white">
            Buy Now
          </Link>
        </button>
      </div>

      {similarProducts && similarProducts.length > 0 && (
        <div className="py-14 flex flex-col gap-2 w-full">
          <p className="section-text">Similar Products</p>
          <div className="flex flex-wrap gap-10 mt-7 w-full">
            {similarProducts.map((similarProduct) => (
              <ProductCard key={similarProduct._id} product={similarProduct} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductDetails;
