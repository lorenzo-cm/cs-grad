import axios from "axios";

import Message from "../models/message";
import { generateUrlSafeRandomString } from "./utils";

export async function createMessage(text_: string, isBot_: boolean, username: string): Promise<boolean> {
    const url = `http://localhost:3001/api/messages/`;
    const postData = {
        text: text_.replace(/\//g, ' '),
        is_bot: isBot_,
        username: username
    };

    try {
        const response = await axios.post(url, postData, {
            withCredentials: true,
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.status >= 200 && response.status < 300) {
            console.log('Message created:', response.data);
            return true;
        } else {
            console.log('Failed to create message:', response.status);
            return false;
        }
    } catch (error) {
        return false;
    }
}



export async function getMessages(username: string): Promise<Message[]> {
    try {
        const response = await axios.get(`http://localhost:3001/api/messages/${username}`, 
                        { withCredentials: true, headers: { 'Content-Type': 'application/json' }});

        if(response.status >= 400){
            return []
        }

        return response.data as Message[]
    } 
    
    catch (error) {
        return [];
    }

}


export const sendMessageAPI = async (prompt: string, username: string): Promise<any> => {
    // Encode the parameters to ensure they are safe for URL usage
    const encodedPrompt = encodeURIComponent(prompt.replace(/\//g, ' '));
    const encodedUsername = encodeURIComponent(username);

    // Construct the URL with the encoded parameters
    const url = `http://localhost:3003/api/prompt=${encodedPrompt}+username=${encodedUsername}`;

    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return []
        }
    }
};


export const sendMessageAPINoUsername = async (prompt: string): Promise<any> => {
    // Encode the parameters to ensure they are safe for URL usage
    const encodedPrompt = encodeURIComponent(prompt.replace(/\//g, ' '));
    const randomUsername = encodeURIComponent(generateUrlSafeRandomString(36));

    // Construct the URL with the encoded parameters
    const url = `http://localhost:3003/api/prompt=${encodedPrompt}+username=~~~~${randomUsername}`;

    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return []
        }
    }
};
