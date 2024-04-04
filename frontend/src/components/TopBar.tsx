import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import logo from '../../assets/logo.svg'; // Adjust the path according to your project structure

import { isLoggedIn, getUser } from '../utils/utils.ts';
import { User } from '../utils/model/user.ts';

const TopBar: React.FC = () => {
  const navigate = useNavigate(); // Initialize useNavigate hook
  const [user, setUser] = useState<User>();

  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const checkAndFetchUser = async () => {
      setLoading(true); // Start loading before the async operations
  
      try {
        const loggedIn = await isLoggedIn();
        if (loggedIn) {
          const userData = await getUser();
          setUser(userData); // Set user data if loggedIn is true
        }
      } catch (error) {
        console.error('Failed to load user data:', error);
      } finally {
        setLoading(false); // Stop loading after all async operations are complete
      }
    };
  
    checkAndFetchUser();
  }, [navigate]);
  
  const handleLoginClick = () => {
    navigate('/login'); // Navigate to login page on button click
  };

  return (
    <div className="flex items-center justify-between p-4 shadow-md bg-blue-950">
      {/* Logo Section */}
      <div className="flex justify-start flex-grow">
        <img src={logo} alt="Logo" className="h-8" />
      </div>

      {/* brand name section */}
      <div className='font-bold text-2xl text-center text-white'>
        Alia chat
      </div>
  
      {/* Login Button/Spacer Section */}
      <div className="flex justify-end flex-grow">
        {!isLoggedIn ? (
          <button
            onClick={handleLoginClick}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded z-30">
            Login
          </button>
        ) : (
          loading ? (
            <div className='text-white mx-2'>Loading...</div>
          ) : (
            <button className="py-2 px-4 text-white bg-indigo-700 rounded" onClick={() => navigate('/profile')}>
              Olá, {user?.name}
            </button>
          )
        )}
      </div>

    </div>
  );
  
};

export default TopBar;
