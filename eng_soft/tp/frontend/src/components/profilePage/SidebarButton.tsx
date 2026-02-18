import React from 'react';

// Button Props Interface
interface SidebarButtonProps {
  icon: string;
  label: string;
  changeSection: () => void; // Passes the function directly
}

const SidebarButton: React.FC<SidebarButtonProps> = ({ icon, label, changeSection }) => (
  <button className="flex items-center p-2 space-x-2 hover:bg-gray-900 rounded-md border border-transparent hover:border-gray-700" onClick={changeSection}>
    <img src={icon} alt={label} className="w-6 h-6 mr-2" />
    <span>{label}</span>
  </button>
);

export default SidebarButton;
