import pool from './db.js';

export const getUserIdBySessionId = async (sessionId) => {
    const result = await pool.query(
        'SELECT user_id FROM tp_es.user_sessions WHERE session_token = $1',
        [sessionId]
    );
    return result.rows[0];
};


export const checkValidSession = async (sessionId) => {
    const result = await pool.query(
        'SELECT user_id FROM tp_es.user_sessions WHERE session_token = $1 AND expires_at > NOW()',
        [sessionId]
    );

    if (result.rows.length === 0) {
        // Nenhuma sessão válida encontrada
        return null;
    }
    return result.rows[0];
}


export const deleteInvalidSessions = async (sessionId) => {
    await pool.query(
        'DELETE FROM tp_es.user_sessions WHERE session_token = $1 AND expires_at < NOW()',
        [sessionId]
    );
}


export const deleteSessionById = async (sessionId) => {
    await pool.query(
        'DELETE FROM tp_es.user_sessions WHERE session_token = $1',
        [sessionId]
    )
}