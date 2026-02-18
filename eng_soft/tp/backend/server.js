import dotenv from 'dotenv';
dotenv.config({path: "../../.env"});

import cookieParser from 'cookie-parser';
import express from 'express';
import cors from 'cors';

import userRouter from './routers/userRouter.js';
import sessionRouter from './routers/sessionRouter.js';
import messagesRouter from './routers/messagesRouter.js';

const app = express();

app.use(cookieParser());

var corsOptions = {
    origin: ["http://localhost:3000", 'http://localhost:3001', 'http://localhost:5173', 'http://localhost:3003'],
    credentials: true
};

app.use(cors(corsOptions));

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", req.header('Origin'));
    res.header("Access-Control-Allow-Credentials", true);
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    res.header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE");
    next();
  });

app.use(express.json());

app.use('/api/session', sessionRouter);
app.use('/api/users', userRouter);
app.use('/api/messages', messagesRouter)

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));