// src/types/productTypes.js

// Notification types as a constant object
export const NotificationType = {
  WELCOME: "WELCOME",
  CHANGE_OF_STOCK: "CHANGE_OF_STOCK",
  LOWEST_PRICE: "LOWEST_PRICE",
  THRESHOLD_MET: "THRESHOLD_MET",
};

// Function to create a product object (to simulate structure)
export const createProduct = ({
  _id,
  url,
  currency,
  image,
  title,
  currentPrice,
  originalPrice,
  priceHistory = [],
  highestPrice,
  lowestPrice,
  averagePrice,
  discountRate,
  description,
  category,
  reviewsCount,
  stars,
  isOutOfStock,
  users = [],
}) => ({
  _id,
  url,
  currency,
  image,
  title,
  currentPrice,
  originalPrice,
  priceHistory,
  highestPrice,
  lowestPrice,
  averagePrice,
  discountRate,
  description,
  category,
  reviewsCount,
  stars,
  isOutOfStock,
  users,
});
