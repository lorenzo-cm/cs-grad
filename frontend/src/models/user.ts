export interface User {
    id: number; // SERIAL se torna number em TypeScript
    username: string; // VARCHAR(255) é uma string
    email: string; // VARCHAR(255) também é uma string
    password: string; // VARCHAR(255) representa a senha como string
    name: string; // VARCHAR(255) para o nome do usuário
    role?: string; // VARCHAR(50) é opcional, representado por '?'
    confirmation_code?: string; // VARCHAR(255) pode ser null/undefined, portanto é opcional
    created_at: Date; // TIMESTAMP WITH TIME ZONE é traduzido para Date
    updated_at: Date; // TIMESTAMP WITH TIME ZONE também é traduzido para Date
  }
  