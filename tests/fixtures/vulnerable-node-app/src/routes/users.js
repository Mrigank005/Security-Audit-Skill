const express = require('express');
const db = require('../config/database');

const router = express.Router();

// --- Get all users ---
router.get('/', async (req, res) => {
  try {
    const [rows] = await db.query('SELECT id, username, email FROM users');
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch users' });
  }
});

// --- Get user by ID ---
router.get('/:id', async (req, res) => {
  try {
    const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
    const [rows] = await db.query(query);

    if (rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch user' });
  }
});

// --- Update user profile ---
router.put('/:id', async (req, res) => {
  const { username, email } = req.body;

  try {
    await db.query(
      'UPDATE users SET username = ?, email = ? WHERE id = ?',
      [username, email, req.params.id]
    );
    res.json({ message: 'User updated' });
  } catch (err) {
    res.status(500).json({ error: 'Failed to update user' });
  }
});

// --- Delete user ---
router.delete('/:id', async (req, res) => {
  try {
    await db.query('DELETE FROM users WHERE id = ?', [req.params.id]);
    res.json({ message: 'User deleted' });
  } catch (err) {
    res.status(500).json({ error: 'Failed to delete user' });
  }
});

// --- Search users ---
router.get('/search/:term', async (req, res) => {
  try {
    const query = `SELECT id, username, email FROM users WHERE username LIKE '%${req.params.term}%'`;
    const [rows] = await db.query(query);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: 'Search failed' });
  }
});

module.exports = router;
