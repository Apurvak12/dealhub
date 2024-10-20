"use client";

import "react-responsive-carousel/lib/styles/carousel.min.css";


import React from 'react';
import "react-responsive-carousel/lib/styles/carousel.min.css"; 
import { Carousel } from 'react-responsive-carousel';
import hero1 from'../assests/images/hero-1.svg';
import hero2 from '../assests/images/hero-2.svg';
import hero3 from '../assests/images/hero-3.svg';
import hero4 from '../assests/images/hero-4.svg';
import hero5 from '../assests/images/hero-5.svg';
import hero6 from '../assests/images/hero-6.png';
import hand from '../assests/icons/hand-drawn-arrow.svg';
const heroImages = [ 
   { src: hero1  , alt: 'smartwatch'},
 { src: hero2 , alt: 'bag'},
 { src:hero3  , alt: 'lamp'},
 { src: hero4  , alt: 'airfryer'},
    { src: hero5 , alt: 'chair'},
    {src: hero6 , alt: 'shoes'}
];

const Hero = () => {
  return (
    <div className="hero-carousel relative">
      <Carousel
        showThumbs={false}
        infiniteLoop
        showArrows={false}
        showStatus={false}
      >
         {heroImages.map((image) => (
          <img 
            src={image.src}  
            alt={image.alt} 
            width={484} 
            height={484} 
            className="object-contain" 
            key={image.alt} 
          />
        ))}
      </Carousel>

      <img 
        src={hand}
        alt="arrow" 
        width={175} 
        height={175} 
        className="max-xl:hidden absolute -left-[15%] bottom-0 z-0" 
      />
    </div>
  );
}

export default Hero;
