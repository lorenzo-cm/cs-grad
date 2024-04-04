import express from 'express';

import { createMessage, getMessagesbyUserId } from '../db/messagesFunctions.js';
import { authSessionMiddleware } from '../session/sessionManager.js';


async function getMessagesRouter(req, res){
    try {


        
    } catch (error) {
        res.status(400).send(error)
    }
}


async function createMessageRouter(req, res){
    try {


        
    } catch (error) {
        res.status(400).send(error)
    }
}


const router = express.Router();

router.use(authSessionMiddleware)

router.get('/history', getMessagesRouter);
router.post('/', createMessageRouter);

export default router;