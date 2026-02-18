import pool from './db.js';

export const createUser = async (username, email, password, name, role, confirmationCode) => {
    const result = await pool.query(
        'INSERT INTO tp_es.users (username, email, password, name, role, confirmation_code) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *',
        [username, email, password, name, role, confirmationCode]
    );
    return result.rows[0];
};

export const getUserByUsername_ = async (username) => {
    const result = await pool.query(
        'SELECT * FROM tp_es.users WHERE username = $1',
        [username]
    );
    return result.rows[0];
};


export const getUserById_ = async (id) => {
    const result = await pool.query(
        'SELECT * FROM tp_es.users WHERE id = $1',
        [id]
    );
    return result.rows[0];
};


export const getUserIdByUsername = async (username) => {
    const result = await pool.query(
        'SELECT id FROM tp_es.users WHERE username = $1',
        [username]
    );
    return result.rows[0].id;
}


export const alterUserDB_ = async (userId, name, role) => {
    try {
        const result = await pool.query(
            'UPDATE tp_es.users SET name = $1, role = $2 WHERE id = $3 RETURNING *',
            [name, role, userId]
        );
        return result.rows[0];
    } catch (error) {
        console.error('Failed to update user:', error);
    }
};