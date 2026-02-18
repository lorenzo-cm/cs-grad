import React from 'react';
import FooterSidebar from './FooterSidebar';
import SidebarButton from './SidebarButton';


import UserIcon from '../../../assets/user.svg';
import UploadIcon from '../../../assets/upload.svg';
import { User } from '../../models/user';

interface SidebarProps {
  handleSectionSelect: (section: string) => void;
  toggleSidebar: () => void;
  user: User;
}

const Sidebar: React.FC<SidebarProps> = ({toggleSidebar, handleSectionSelect, user }) => {
  return (
    <aside className="w-64 h-full" aria-label="Sidebar">
      <div className="flex flex-col h-full overflow-y-auto py-4 px-3 rounded bg-gray-800">
        
        {/* Main content area - allow it to grow and fill available space */}
        <div className="flex-1">

          {/* upper */}
          <div className='flex flex-row text-center content-center mb-5'>

            <button className="md:hidden flex flex-col justify-center items-center w-10 h-10 rounded focus:outline-none" onClick={toggleSidebar}>
              <span className="hamburger-line"></span>
              <span className="hamburger-line"></span>
              <span className="hamburger-line"></span>
            </button>

            <div className='flex items-center font-bold text-2xl mx-2 text-center content-center'>
              Alia chat 
            </div>
            
          </div>

          <div className="flex flex-col space-y-2">
            <SidebarButton 
              icon={UserIcon} 
              label="Configurações" 
              changeSection={() => handleSectionSelect('user')} 
            />
            <SidebarButton 
              icon={UploadIcon} 
              label="Upload PDF" 
              changeSection={() => handleSectionSelect('upload')} 
            />
            {/* More buttons as needed */}
          </div>
        </div>
        
        {/* Footer - It will not grow but stay at the bottom */}
        <div>
          <FooterSidebar user={user} />
        </div>

      </div>
    </aside>
  );
};


export default Sidebar;
