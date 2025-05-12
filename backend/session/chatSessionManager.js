import { v4 } from 'uuid';

export function createChatSession(req, res){
    const chatSessionToken = v4();

    res.cookie('chat_session_id', chatSessionToken, {
        httpOnly: true,
        secure: true,
        maxAge: 1000 * 60 * 60 * 24, // Cookie expires in 1 day
        sameSite: 'lax',
        domain: 'localhost',
    });


    return chatSessionToken
}