import React from 'react';
import { Link } from 'react-router-dom'; // Use this for React Router
import { Product } from '../types/productTypes'; // Ensure this path is correct

interface Props {
    product: Product;
}

const ProductCard: React.FC<Props> = ({ product }) => {
    return (
        <Link to={`/products/${product._id}`} className="product-card"> {/* Correctly using 'to' for react-router */}
            <div className='product-card_img-container'>
                <img // Use a regular <img> tag for React
                    src={product.image}
                    alt={product.title}
                    className="product-card_img"
                    style={{ width: '200px', height: '200px' }} // Inline styles for width and height
                />
            </div>
            <div className='flex flex-col gap-3'> {/* Removed extra quotes around className */}
                <h3 className='product-title'>{product.title}</h3>
                <div className='flex justify-between'>
                    <p className='text-black opacity-50 text-lg capitalize'>
                        {product.category}
                    </p>
                    <p className="text-black text-lg font-semibold">
                        <span>{product.currency}</span>
                        <span>{product.currentPrice}</span>
                    </p>
                </div>
            </div>
        </Link>
    );
};

export default ProductCard;
