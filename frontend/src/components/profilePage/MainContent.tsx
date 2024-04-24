import React, { useState } from "react";
import { User } from "../../models/user";

import UploadSection from "./UploadSection";
import { alterUserDB } from "../../utils/utils";

interface MainContentProps {
  section: string;
  user: User|undefined;
}

interface UserProfileProps {
  user: User;
}

interface OkMsg {
  text: string;
  suc: boolean;
}

const UserProfile: React.FC<UserProfileProps> = ({ user }) => {
  // State for form inputs
  const [name, setName] = useState<string>(user.name);
  const [role, setRole] = useState<string>(user.role ?? '');
  const [okMsg, setOkMsg] = useState<OkMsg>({ text: '', suc: true });

  // Handle form submission
  const handleSubmit = async (event: React.MouseEvent<HTMLButtonElement, MouseEvent>): Promise<void> => {
    event.preventDefault();
    try {
      // Assuming alterUserDB is defined elsewhere and accepts a User object
      await alterUserDB({ ...user, name, role });
      setOkMsg({ text: 'Profile updated successfully!', suc: true});
    } catch (error) {
      console.error('Failed to update user:', error);
      setOkMsg({text: 'Oh, oh, something went wrong', suc: false})
    }
  };

  // Function to clear the okMsg
  const handleCloseMsg = () => {
    setOkMsg({ text: '', suc: true });
  };

  return (
    <div>
      <h1 className="font-bold text-xl mb-2">User Profile</h1>
      <p><strong>Username:</strong> {user.username}</p>
      <p><strong>Name:</strong> 
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="ml-2 border rounded p-1"
        />
      </p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Role:</strong>
        <input
          type="text"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="ml-2 border rounded p-1"
        />
      </p>
      <button
        onClick={handleSubmit}
        className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Update Profile
      </button>

      {okMsg.text && (
        <div className={`mt-8 w-72 px-4 py-3 rounded relative ${okMsg.suc ? 'bg-green-100 border-green-400 text-green-700' : 'bg-red-100 border-red-400 text-red-700'}`} role="alert">
          <span className="block sm:inline">{okMsg.text}</span>
          <span
            className="absolute top-0 bottom-0 right-0 px-4 py-3"
            onClick={handleCloseMsg}
            style={{ cursor: 'pointer' }}
          >
            <svg className={`fill-current h-6 w-6 ${okMsg.suc ? 'text-green-500' : 'text-red-600'} text-center`} role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
              <title>Close</title>
              <path d="M14.348 14.849a1.2 1.2 0 01-1.697 0L10 11.196 7.349 14.849a1.2 1.2 0 01-1.697-1.697L8.196 10 5.652 7.349a1.2 1.2 0 111.697-1.697L10 8.804l2.651-3.152a1.2 1.2 0 111.697 1.697L11.804 10l2.544 2.651a1.2 1.2 0 010 1.698z"/>
            </svg>
          </span>
        </div>
      )}

    </div>
  );
};


export const MainContent: React.FC<MainContentProps> = ({ section, user }) => {
  let content;
  switch (section) {
    case 'user':
      content = user ? <UserProfile user={user} /> : <div>Loading...</div>;
      break;
    case 'upload':
      content = <UploadSection />;
      break;
    default:
      content = <div>Section not found</div>;
  }

  return <div className="p-4">{content}</div>;
};
