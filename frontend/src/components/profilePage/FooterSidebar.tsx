// src/components/LogoutButton.tsx
import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { User } from '../../models/user';

interface FooterSidebarProps {
  user: User;
}

const FooterSidebar: React.FC<FooterSidebarProps> = ({ user }) => {
  const navigate = useNavigate();


  const logoutUser = async () => {
    try {
      await axios.post('http://localhost:3001/api/users/logout', {}, {
                        withCredentials: true,
                        headers: { 'Content-Type': 'application/json' }
                      });
      return true;
    } catch (error) {
      console.error('Logout failed:', error);
      return false;
    }
  };


  const handleLogout = async () => {
    if (await logoutUser()) {
      navigate('/')
    }
  };

  return (
    <div className="bottom w-full text-white p-0 m-0 ">

      <button className='font-bold mb-4 p-2 w-full text-green-500 hover:bg-gray-700 rounded-md border border-transparent hover:border-gray-700'
              onClick={() => navigate(`/chat/${user.username}`)}>
        Chat Area
      </button>

      <button onClick={handleLogout} className='font-bold mb-4 p-2 w-full
                                               hover:bg-gray-900 rounded-md border border-transparent hover:border-gray-700'>Logout</button>

      <div className='flex justify-center items-center w-full text-center'>

        <button className="flex items-center p-2 mr-4 space-x-2 hover:bg-gray-900 rounded-md border border-transparent hover:border-gray-700"
                  onClick={() => navigate('/')}>
          <img src="../assets/logo.svg" alt="Logo" className="h-8" />
        </button>

        <a href="https://github.com/lorenzo-cm" className='flex items-center justify-center p-2 hover:bg-gray-900 rounded-md border border-transparent hover:border-gray-700' 
            target="_blank" rel="noopener noreferrer">GitHub</a>

      </div>


    </div>
  );
};

export default FooterSidebar;
