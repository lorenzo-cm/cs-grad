export default interface Message {
    id: number;
    chat_id?: number;
    user_id?: number;
    is_bot: boolean;
    text: string;
    sent_at: string;
    status?: string;
}

// CREATE TABLE tp_es.messages (
//     id SERIAL PRIMARY KEY,
//   	chat_id UUID NOT NULL,
//     user_id INTEGER NOT NULL,
//   	is_bot BOOLEAN NOT NULL,
//     text TEXT,
//     sent_at TIMESTAMP
// );