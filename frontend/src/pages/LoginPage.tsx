import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { motion } from 'framer-motion';

import { isLoggedIn } from '../utils/utils.ts'
import performUserLogin from '../utils/performUserLogin.ts';

// Atualizando a interface para incluir todos os campos

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    isLoggedIn().then((loggedIn) => {
      if(loggedIn){
        navigate('/profile')
      }
    })
  }, [navigate]);


  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    performUserLogin(username, password, navigate, setErrorMessage)

  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex justify-center items-center h-screen">
        <div className="absolute top-5 left-5"> {/* Position the back button */}
          <button onClick={() => navigate('/')} className="text-2xl">
            ← {/* Stylish left arrow as a back button */}
          </button>
        </div>
        <form onSubmit={handleSubmit} className="w-full max-w-xs">
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">Username</label>
            <input type="text" id="email" value={username} onChange={(e) => setUsername(e.target.value.replace(/\s+/g, ''))}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
          </div>
          <div className="mb-6">
            <label htmlFor="password" className="block text-gray-700 text-sm font-bold mb-2">Password</label>
            <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" />
          </div>
          <div className="flex items-center justify-between">
            <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
              Sign In
            </button>

            <button onClick={() => navigate('/register')} type='button' className="bg-blue-950 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
              Sign Up
            </button>
          </div>

          <div className="my-5 mx-6 flex items-center justify-center bg-red-200 rounded">
            {errorMessage && <div className="text-red-700 ">{errorMessage}</div>}
          </div>
            
        </form>
      </div>
    </motion.div>
  );
};

export default LoginPage;
