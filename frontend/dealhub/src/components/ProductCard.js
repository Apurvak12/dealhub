import React from 'react';
import { Link } from 'react-router-dom';

const ProductCard = ({ product }) => {
    return (
        <Link 
            to={`/products/${product?._id}`}  // Fixed template literal syntax
            className="product-card" 
            aria-label={`View details for ${product?.title}`} // Fixed template literal syntax
        >
            <div className='product-card_img-container'>
                <img
                    src={product?.image || '/placeholder.jpg'} // Fallback image if none provided
                    alt={product?.title || 'Product image'}
                    className="product-card_img"
                    style={{ width: '200px', height: '200px' }} // Inline styles for width and height
                />
            </div>
            <div className='flex flex-col gap-3'>
                <h3 className='product-title'>{product?.title || 'No title available'}</h3>
                <div className='flex justify-between'>
                    <p className='text-black opacity-50 text-lg capitalize'>
                        {product?.category || 'Uncategorized'}
                    </p>
                    <p className="text-black text-lg font-semibold">
                        <span>{product?.currency || '$'}</span>
                        <span>{product?.currentPrice?.toFixed(2) || 'N/A'}</span>
                    </p>
                </div>
            </div>
        </Link>
    );
};

export default ProductCard;
