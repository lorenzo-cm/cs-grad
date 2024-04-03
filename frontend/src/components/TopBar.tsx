// src/components/TopBar.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import logo from '../../assets/logo.svg'; // Adjust the path according to your project structure

const TopBar: React.FC = () => {
  const isLoggedIn = false; // Placeholder for authentication state
  const navigate = useNavigate(); // Initialize useNavigate hook

  const handleLoginClick = () => {
    navigate('/login'); // Navigate to login page on button click
  };

  return (
    <div className="relative flex items-center p-4 shadow-md bg-blue-950">
      <img src={logo} alt="Logo" className="h-8" />
  
      <div className='absolute inset-0 flex justify-center items-center'>
        <div className='font-bold text-2xl text-center text-white'>
          Alia chat
        </div>
      </div>
  
      {/* Only show the login button if not logged in, but always occupy space with an invisible spacer for balance */}
      <div className="ml-auto">
        {!isLoggedIn ? (
          <button
            onClick={handleLoginClick}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Login
          </button>
        ) : (
          <div className="py-2 px-4"> {/* Invisible spacer with the same padding as the button */}
          </div>
        )}
      </div>
    </div>
  );
  
};

export default TopBar;
