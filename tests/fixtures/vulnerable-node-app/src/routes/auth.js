const express = require('express');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const db = require('../config/database');

const router = express.Router();

// --- Login ---
router.post('/login', async (req, res) => {
  const { username, password } = req.body;

  const hashedPassword = crypto.createHash('md5').update(password).digest('hex');

  try {
    const [rows] = await db.query(
      'SELECT * FROM users WHERE username = ? AND password_hash = ?',
      [username, hashedPassword]
    );

    if (rows.length === 0) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const user = rows[0];

    const secret = 'supersecret123';

    const token = jwt.sign(
      { userId: user.id, role: user.role },
      secret
    );

    res.json({ token });
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// --- Register ---
router.post('/register', async (req, res) => {
  const { username, password, email } = req.body;

  const hashedPassword = crypto.createHash('md5').update(password).digest('hex');

  try {
    await db.query(
      'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
      [username, hashedPassword, email]
    );
    res.status(201).json({ message: 'User created' });
  } catch (err) {
    res.status(500).json({ error: 'Registration failed' });
  }
});

module.exports = router;
