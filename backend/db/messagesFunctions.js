import pool from './db.js';

export const createMessage = async (text, idReceiver, idSender) => {
  try {
    const insertMessageQuery = `
      INSERT INTO tp_es.messages (sender_id, receiver_id, content)
      VALUES ($1, $2, $3)`;
    await client.query(insertMessageQuery, [idSender, idReceiver, text]);

    client.release();
  } catch (error) {
    console.error(`createMessage Error: ${error.message}`);
    throw error;
  }
};


export const getMessagesbyUserId = async (userId_receiver, userId_sender) => {
    try {
      const client = await pool.connect();
  
      const usersQuery = `
        SELECT m.content, m.sent_at
        FROM tp_es.messages m
        WHERE (m.sender_id = $1 AND m.receiver_id = $2)
           OR (m.sender_id = $2 AND m.receiver_id = $1)
        ORDER BY m.sent_at ASC`;
  
      const { rows } = await client.query(usersQuery, [userId_sender, userId_receiver]);
  
      client.release();
  
      return rows;
    } catch (error) {
      console.error(`getMessages Error: ${error.message}`);
      throw error;
    }
  };
  

export const getMessagesbyUsername = async (username_receiver, username_sender) => {
  try {
    const client = await pool.connect();

    const usersQuery = `
      SELECT m.content, m.sent_at
      FROM tp_es.messages m
      JOIN tp_es.users sender ON m.sender_id = sender.id
      JOIN tp_es.users receiver ON m.receiver_id = receiver.id
      WHERE (sender.username = $1 AND receiver.username = $2)
         OR (sender.username = $2 AND receiver.username = $1)
      ORDER BY m.sent_at ASC`;

    const { rows } = await client.query(usersQuery, [username_sender, username_receiver]);

    client.release();

    return rows;
  } catch (error) {
    console.error(`getMessages Error: ${error.message}`);
    throw error;
  }
};
