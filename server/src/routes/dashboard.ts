import express from 'express';

const router = express.Router();

router.post('/dashboard', signupUser);

export default router;
