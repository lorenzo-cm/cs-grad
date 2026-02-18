# Trabalho Prático - Teste de Software - Wordle

## Grupo
- Gabriel Pains de Oliveira Cardoso
- Lorenzo Carneiro Magalhães
- Victor de Almeida Nunes Murta

Este repositório contém o projeto do jogo Wordle/Termo, desenvolvido como trabalho para a disciplina de Teste de Software.

---

## Estrutura do Projeto

- `backend/` — API em Python (FastAPI)
- `frontend/` — Interface web (Next.js + React)

---

## Backend

API simples para o jogo Wordle/Termo em Python usando FastAPI.

### Como Executar o Backend

```bash
cd backend
pip install -r requirements.txt
python run_server.py
```

Servidor: `http://localhost:8000`

Documentação: `http://localhost:8000/docs`

### Endpoints

**Criar Jogo**
```
POST /api/v1/wordle/games
```

**Fazer Tentativa**
```
POST /api/v1/wordle/games/{game_id}/guess
Body: {"word": "carro"}
```

**Ver Estado do Jogo**
```
GET /api/v1/wordle/games/{game_id}
```

### Funcionalidades

- Criação de jogos com IDs simples (1, 2, 3...)
- Validação de palavras de 5 letras
- Sistema de feedback: "correct", "present", "not present"
- Máximo 6 tentativas por jogo
- Palavra revelada quando o jogo termina

### Tecnologias Backend
- FastAPI
- Pydantic
- Pytest
- Uvicorn

---

## Frontend

Interface web desenvolvida com Next.js e React.

### Como Executar o Frontend

```bash
cd frontend
npm install
npm run dev
```

A aplicação estará disponível em: `http://localhost:3000`

### Tecnologias Frontend
- Next.js
- React
- Chakra UI
- TypeScript

---

### Como testar o Backend

Instale as dependências conforme mostrado acima.
A partir do diretório raiz, execute

```bash
pytest --cov=backend --cov-branch --cov-report=xml backend/
```

### Como testar o Frontend (E2E)

Garanta que o front e back estejam rodando de acordo com os comandos descritos em "Como Executar".
Depois execute:

```bash
cd frontend
npx playwright install
npx playwright test --config=playwright.config.ts
```
