import axios from "axios";

import { User } from "../models/user";

export async function isLoggedIn() {
    try {
        const response = await fetch('http://localhost:3001/api/session/check', {
            method: 'GET', // Make sure this matches your backend route method
            credentials: 'include', // Needed to include cookies
        });

        if (response.ok) {
            console.log("Session is valid.");
            return true;
        } else if (response.status === 401) {
            // Here we read the response text which contains our custom message
            const errorMessage = await response.text(); // Use .json() if you're sending JSON
            console.error("Error verifying session:", errorMessage);
            return false;
        } else {
            console.error("Unexpected response from server:", response);
            return false;
        }

    } catch (error) {
        console.error("Error in isLoggedIn function:", error);
        return false;
    }
}

export async function getUser(): Promise<User> {
    try {
        const response = await axios.get('http://localhost:3001/api/users/', { withCredentials: true, headers: { 'Content-Type': 'application/json' }});
        return response.data as User;

    } 
    
    catch (error) {
        console.error('Error fetching user:', error);
        throw error;
    }

}


export async function getUsernameBySession(): Promise<string> {
    try {
        const response = await axios.get('http://localhost:3001/api/users/', { withCredentials: true, headers: { 'Content-Type': 'application/json' }});
        return response.data['username'];

    } 
    
    catch (error) {
        console.error('Error fetching user:', error);
        return '';
    }

}


export async function alterUserDB(user: User): Promise<User> {
    try {
        const response = await axios.post('http://localhost:3001/api/users/alter', user, {
            withCredentials: true,
            headers: { 'Content-Type': 'application/json' }
        });
        return response.data as User;
    } catch (error) {
        console.error('Error updating user:', error);
        throw error;
    }
}


export function generateUrlSafeRandomString(length: number): string {
    // Define a set of characters that are safe for URL usage
    const urlSafeChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
    const charArray = new Uint8Array(length);
    window.crypto.getRandomValues(charArray); // Generate random values
    let randomString = '';

    // Convert each byte into a character from the URL-safe characters
    for (let i = 0; i < length; i++) {
        randomString += urlSafeChars.charAt(charArray[i] % urlSafeChars.length);
    }

    return randomString;
}


