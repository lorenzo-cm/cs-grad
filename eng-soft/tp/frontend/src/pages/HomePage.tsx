import React from 'react';
import TopBar from '../components/TopBar';
import ChatArea from '../components/ChatArea';

const Home: React.FC = () => {
  return (
    <div className="flex flex-col h-screen">
      <TopBar />
      <ChatArea />
    </div>
  );
};

export default Home;
