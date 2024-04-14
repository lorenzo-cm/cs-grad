import pool from './db.js';

export const createMessage = async (text, userId, chatId, isBot) => {
  try {
    const insertMessageQuery = `
      INSERT INTO tp_es.messages (user_id, is_bot, text, chat_id)
      VALUES ($1, $2, $3, $4) returning *`;
    const result = await pool.query(insertMessageQuery, [userId, isBot, text, chatId]);
    return result.rows[0];

  } catch (error) {
    console.error(`createMessage Error: ${error.message}`);
    throw error;
  }
};


export const getMessagesbyUserId = async (userId, chatId) => {
    try {  
      const usersQuery = `
        SELECT text, sent_at
        FROM tp_es.messages
        WHERE user_id = $1 AND chat_id = $2
        ORDER BY sent_at ASC`;
  
      const { rows } = await pool.query(usersQuery, [userId, chatId]);
      return rows;

    } catch (error) {
      console.error(`getMessages Error: ${error.message}`);
      throw error;
    }
};
  

export const getMessagesByUsername = async (username, chatId) => {
    try {
      const messagesQuery = `
        SELECT m.id, m.text, m.sent_at, m.is_bot
        FROM tp_es.messages m
        JOIN tp_es.users u ON m.user_id = u.id
        WHERE u.username = $1 AND m.chat_id = $2
        ORDER BY m.sent_at ASC`;

      const { rows } = await pool.query(messagesQuery, [username, chatId]);
      return rows;

    } catch (error) {
      console.error(`getMessages Error: ${error.message}`);
      throw error;
    }
};