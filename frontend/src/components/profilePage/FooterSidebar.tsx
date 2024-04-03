// src/components/LogoutButton.tsx
import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const FooterSidebar: React.FC = () => {
  const navigate = useNavigate();


  const logoutUser = async () => {
    try {
      const response = await axios.post('http://localhost:3001/api/users/logout', {}, {
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
    <div className="bottom w-full text-white p-0 m-0">
      <button onClick={handleLogout} className='font-bold mb-4'>Logout</button>
      <div className='flex content-center text-center'>
        <img src="../assets/logo.svg" alt="Logo" className="h-8 pr-4" />
        <a href="https://github.com/lorenzo-cm" className='content-center text-center' target="_blank" rel="noopener noreferrer">GitHub</a>
      </div>
    </div>
  );
};

export default FooterSidebar;
