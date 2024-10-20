import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../assests/icons/logo.svg';
import searchIcon from '../assests/icons/search.svg';
import heartIcon from '../assests/icons/black-heart.svg';
import userIcon from '../assests/icons/user.svg';

const navIcons = [
  { src: searchIcon, alt: 'search' },
  { src: heartIcon, alt: 'heart' },
  { src: userIcon, alt: 'user' },
];

const Navbar = () => {
  return (
    <header className="w-full">
      <nav className="nav">
        <Link to="/" className="flex items-center gap-1">
          <img 
            src={logo}
            width={27}
            height={27}
            alt="logo"
          />
          <p className="nav-logo">
            Deal<span className='text-primary'>HUB</span>
          </p>
        </Link>

        <div className="flex items-center gap-5">
          {navIcons.map((icon) => (
            <img 
              key={icon.alt}
              src={icon.src}
              alt={icon.alt}
              width={28}
              height={28}
              className="object-contain"
            />
          ))}
        </div>
      </nav>
    </header>
  );
}

export default Navbar;

