import axios from "axios";

import Message from "../models/message";


export async function createMessage(text_: string, isBot_: boolean, username: string): Promise<boolean> {
    const url = `http://localhost:3001/api/messages/`;
    const postData = {
        text: text_,
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



export async function getMessages(username: string): Promise<any[]> {
    try {
        const response = await axios.get(`http://localhost:3001/api/messages/${username}`, 
                        { withCredentials: true, headers: { 'Content-Type': 'application/json' }});
        console.log(response.data)
        return response.data as Message[]
    } 
    
    catch (error) {
        return [];
    }

}