import express from 'express';

import { authSession } from '../session/sessionManager.js';

const router = express.Router();

router.get('/check', authSession);

export default router;