import React, { useState } from 'react';

const ProductCard = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [productInfo, setProductInfo] = useState(null);
    const [error, setError] = useState('');

    const handleSearch = async () => {
        try {
            const response = await fetch('http://localhost:5000/search', { // Corrected endpoint to /search
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_name: searchTerm }),  // Updated key to match backend
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setProductInfo(data);
            setError(''); // Clear any previous errors
        } catch (error) {
            console.error('Failed to fetch:', error);
            setError('Failed to fetch product information. Please try again.');
        }
    };

    return (
        <div>
            <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Enter Amazon product name"
            />
            <button onClick={handleSearch}>Search</button>
            {error && <p>{error}</p>}
            {productInfo && (
                <div>
                    <h2>{productInfo.title}</h2>
                    <p>Price: {productInfo.price}</p>
                    <p>Reviews: {productInfo.reviews}</p>
                    <p>Description: {productInfo.description}</p>
                </div>
            )}
        </div>
    );
};

export default ProductCard;
