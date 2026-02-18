import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import logo from '../../assets/logo.svg';

import { isLoggedIn, getUser } from '../utils/utils.ts';
import { User } from '../models/user.ts';

const TopBar: React.FC = () => {
  const navigate = useNavigate();

  let { username } = useParams(); 

  const [user, setUser] = useState<User>();
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const checkAndFetchUser = async () => {
      setLoading(true);
  
      try {
        const loggedIn = await isLoggedIn();
        if (loggedIn) {
          const userData = await getUser();
          setUser(userData);
        }
      } catch (error) {
        console.error('Failed to load user data:', error);
      } finally {
        setLoading(false);
      }
    };
  
    checkAndFetchUser();
  }, [navigate]);

  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="flex items-center justify-between p-4 shadow-md bg-blue-950">
      <div className="flex justify-start flex-grow">
        <img src={logo} alt="Logo" className="h-8" />
      </div>

      

      <div className='font-bold text-2xl text-center text-white'> 
        {username ? <div> <span className='text-green-500'>{username}</span> Chat</div> : <div>Alia Chat</div>}
      </div>
  
      <div className="flex justify-end flex-grow">

        {loading ? (
          <div className='text-white mx-4 my-2'>Loading...</div>
        ) : !user ? (
          <button
            onClick={handleLoginClick}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded z-30">
            Login
          </button>
        ) : (
            <button className="py-2 px-4 text-white bg-blue-700 rounded" onClick={() => navigate('/profile')}>
              Olá, {user?.name}
            </button>
          )
        }

      </div>

    </div>
  );
};

export default TopBar;
