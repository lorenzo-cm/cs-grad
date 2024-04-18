import React from "react";
import { User } from "../../models/user";

import UploadSection from "./UploadSection";

interface MainContentProps {
  section: string;
  user: User|undefined;
}

interface UserProfileProps {
  user: User;
}

const UserProfile: React.FC<UserProfileProps> = ({ user }) => (
  <div>
    <h1 className="font-bold text-xl mb-2">User Profile</h1>
    <p><strong>Name:</strong> {user.username}</p>
    <p><strong>Email:</strong> {user.email}</p>
    <p><strong>Role:</strong> {user.role}</p>
  </div>
);

// const UploadSection = () => <div>Upload Section</div>;

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
