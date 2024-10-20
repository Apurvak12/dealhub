import React from 'react';
import PropTypes from 'prop-types';
//have to install prop-types
//command npm install prop-types



const PriceInfoCard = ({ title, iconSrc, value }) => {
  return (
    <div className="price-info_card p-4 shadow-lg rounded-lg bg-white">
      <p className="text-base text-black-100">{title}</p>

      <div className="flex items-center gap-2 mt-2">
        <img src={iconSrc} alt={title} width={24} height={24} loading="lazy" />
        <p className="text-2xl font-bold text-secondary">{value}</p>
      </div>
    </div>
  );
};

// PropTypes for prop validation
PriceInfoCard.propTypes = {
  title: PropTypes.string.isRequired,
  iconSrc: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
};

export default PriceInfoCard;
