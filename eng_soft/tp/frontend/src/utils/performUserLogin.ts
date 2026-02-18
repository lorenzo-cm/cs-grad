import axios from 'axios';
import { NavigateFunction } from 'react-router-dom';

/**
 * Performs user login.
 * 
 * @param {string} username - The username of the user trying to log in.
 * @param {string} password - The password of the user.
 * @param {NavigateFunction} navigate - The navigate function from useNavigate() hook of React Router.
 * @param {(message: string | object) => void} fnError - A callback function for handling error messages.
 */
const performUserLogin = async (
  username: string,
  password: string,
  navigate: NavigateFunction,
  fnError: (message: string) => void // Adjusted to accept both string and object for error messages
): Promise<void> => { // Indicates that this async function returns a Promise that resolves to void
    try {
        const response = await axios.post('http://localhost:3001/api/users/login', { username, password },
            { withCredentials: true, headers: { 'Content-Type': 'application/json' }});

        console.log('Login Success:', response.data);
        
        // Successful login
        navigate('/profile');

    } catch (error: any) { // Using `any` temporarily; see note below about handling unknown types
        console.error('Login Error:', error);
        
        if (error.response) {
            fnError(error.response.data);

        } else if (error.request) {
            // The request was made but no response was received
            fnError('The request was made but no response was received.');
            
        } else {
            // Something happened in setting up the request
            fnError('An error occurred. Please try again.');
        }
    }
};

export default performUserLogin;