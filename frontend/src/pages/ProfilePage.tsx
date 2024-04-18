import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

import { isLoggedIn, getUser } from '../utils/utils.ts';
import { User } from '../models/user.ts';
import Sidebar from '../components/profilePage/Sidebar.tsx';
import { MainContent } from '../components/profilePage/MainContent.tsx';

const ProfilePage: React.FC = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<User>();
  const [currentSection, setCurrentSection] = useState<string>("user");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    
    const fetchUser = async () => {
      try {
        const userData = await getUser();
        setUser(userData);
      } catch (error) {
        console.error('Failed to load user data:', error);
      }
    };

    isLoggedIn().then((loggedIn) => {
      if(loggedIn){
        fetchUser();
      } else{
        navigate('/login');
      }
    });
  }, [navigate]);

  // Function to toggle the sidebar
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSectionSelect = (section:string) => {
    setIsSidebarOpen(!isSidebarOpen);
    setCurrentSection(section);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex h-screen overflow-hidden">

        <div className={`sidebar w-64 h-full bg-gray-800 text-white fixed inset-y-0 left-0 transform ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} md:relative md:translate-x-0 transition duration-200 ease-in-out`}>
          <Sidebar handleSectionSelect={handleSectionSelect} toggleSidebar={toggleSidebar} user={user!}/>
        </div>

        <main className="flex-grow overflow-auto">

          {/* Header */}

          <header className='flex mt-4 mx-3 bg-indigo-200 lg:bg-white md:bg-white rounded'>

            <button className="md:hidden flex flex-col justify-center items-center w-10 h-10 rounded focus:outline-none" onClick={toggleSidebar}>
              <span className="hamburger-line" style={{ backgroundColor: 'rgb(31 41 55)' }}></span>
              <span className="hamburger-line" style={{ backgroundColor: 'rgb(31 41 55)' }}></span>
              <span className="hamburger-line" style={{ backgroundColor: 'rgb(31 41 55)' }}></span>
            </button>

            <div className='flex items-center font-bold text-2xl mx-2 text-center content-center'>
                Alia chat 
            </div>

          </header>


          {/* Main page */}

          <MainContent section={currentSection} user={user} />

        </main>
      </div>
    </motion.div>
  );

};

export default ProfilePage;