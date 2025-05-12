import React from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';

import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import ProfilePage from './pages/ProfilePage';
import RegisterPage from './pages/RegisterPage';

import './index.css';


const App: React.FC = () => {
  return (
    <BrowserRouter>
      <RouteRenderer />
    </BrowserRouter>
  );
};

const RouteRenderer: React.FC = () => {
  const location = useLocation(); // Obtem a localização atual
  
  return (
    <AnimatePresence mode='wait'>
      <Routes location={location} key={location.pathname}>
        <Route path="/chat/:username" element={<HomePage />} />
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/register" element={<RegisterPage/>} />
      </Routes>
    </AnimatePresence>
  );
}

export default App;
