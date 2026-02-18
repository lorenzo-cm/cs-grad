import { v4 } from 'uuid';
import pool from '../db/db.js';

import { getUserIdBySessionId, checkValidSession, deleteInvalidSessions, deleteSessionById } from '../db/sessionFunctions.js';


export const createSession = async (req, res) => {
    const { user } = req;
    const sessionToken = v4(); // Generate a unique session token
    const userId = user.id; // Assuming you have the user's ID

    try {
        // Insert the session into your database
        await pool.query(
          'INSERT INTO tp_es.user_sessions (session_token, user_id, expires_at) VALUES ($1, $2, NOW() + INTERVAL \'30 days\')',
          [sessionToken, userId]
        );

        // Set the session token as an HTTP-only cookie
        res.cookie('session_id', sessionToken, {
            httpOnly: true,
            secure: true,
            maxAge: 1000 * 60 * 60 * 24 * 30, // Cookie expires in 30 days
            sameSite: 'lax',
            domain: 'localhost',
        });

        // Send back a success response
        res.status(200).json({ sessionToken: sessionToken, message: 'Login bem-sucedido' });

    } catch (error) {
        console.error('Erro ao criar sessão', error);
        res.status(500).json({ message: 'Erro interno do servidor' });
    }
};


async function baseAuth(req, res) {

    try {
        const sessionToken = req.cookies.session_id;

        if (!sessionToken) {
            return {status: 401, message: 'Token not found'}
        }

        const userId = await checkValidSession(sessionToken)

        if (!userId) {
            deleteInvalidSessions(sessionToken)
        
            res.clearCookie('session_id', {
                httpOnly: true,
                secure: true, // Note: Set to false if you're not using https in development
                sameSite: 'lax', // Adjust according to your requirements
                domain: 'localhost', // Set appropriately for production
            });

            return {status: 401, message: 'Token expired'}
        }
        
        // userIs a object alredy and the key from db is user_id
        return {data: userId , status: 200, message: 'Token validated'}
    } 
    
    catch (error) {
        return {status: 500, message: 'Internal server error'}
    }
}

export async function authSession(req, res) {

    console.log("authSession")

    const responseJson = await baseAuth(req, res);

    if (responseJson.hasOwnProperty("data")) {
        req.data = responseJson.data
    }

    res.status(responseJson.status).json({ message: responseJson.message})
}


export async function authSessionMiddleware(req, res, next) {

    console.log("authSessionMiddleware")

    const responseJson = await baseAuth(req, res);

    if (responseJson.hasOwnProperty("data")) {
        req.data = responseJson.data;
        next()
    }

    if (responseJson.status >= 400){
        res.status(responseJson.status).json({ message: responseJson.message})
    }
};


export const authSessionMiddlewareRedirect = async (req, res, next) => {

    const responseJson = await baseAuth(req, res);

    if (responseJson.hasOwnProperty("data")) {
        req.data = responseJson.data
    }

    if (responseJson.status <= 400){
        console.log('redirecting user');
        return res.redirect('/profile');
    }

    next()
};


export const deleteSessionMiddleware = async (req, res, next) => {

    try {
        const sessionToken = req.cookies['session_id'];

        if (!sessionToken) {
            return {status: 401, message: 'User not logged in'}
        }

        res.clearCookie('session_id', {
            httpOnly: true,
            secure: true,
            sameSite: 'lax',
            domain: 'localhost',
        });

        deleteSessionById(sessionToken)

        next()
    } 
    
    catch (error) {
        return {status: 500, message: 'Internal server error'}
    }
};