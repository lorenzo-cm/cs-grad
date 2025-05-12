import express from 'express';

import { createMessage, getMessagesByUsername } from '../db/messagesFunctions.js';
import { createChatSession } from '../session/chatSessionManager.js';

import { getUserIdByUsername } from '../db/userFunctions.js';


async function getMessagesRouter(req, res){
    try {

        const chatSessionId = req.cookies['chat_session_id'];

        if(!chatSessionId){
            return res.json([])
        }

        const username = req.params.username;
        if (!username) {
            return res.send('You must specify a username');
        }

        const messages = await getMessagesByUsername(username, chatSessionId);

        return res.status(200).json(messages);

    } catch (error) {
        console.error(`getMessagesRouter Error: ${error.message}`);
        return res.status(400).send(error.message);
    }
}


async function createMessageUserRouter(req, res){
    try {
        const { text, is_bot, username } = req.body;

        if (!text || is_bot === undefined || !username) {
            return res.status(400).send('You must specify text, is_bot, and username');
        }

        let chatSessionId = req.cookies['chat_session_id'];

        if(!chatSessionId){
            chatSessionId = createChatSession(req, res);
        }

        const userId = await getUserIdByUsername(username)

        if (!userId) {
            return res.status(404).send('User not found');
        }

        const message_object = await createMessage(text, userId, chatSessionId, is_bot);

        res.status(201).json(message_object);

    } catch (error) {
        console.error(`createMessageRouter Error: ${error.message}`);
        res.status(400).send(error.message);
    }
}


const router = express.Router();

router.get('/:username', getMessagesRouter);
router.post('/', createMessageUserRouter);

export default router;