import hashlib
import sqlite3
from flask import Blueprint, request, jsonify, session

auth_bp = Blueprint('auth', __name__)

DATABASE = 'app.db'

SECRET_KEY = 'dev-secret'


def get_db():
    return sqlite3.connect(DATABASE)


# --- Login ---
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    password_hash = hashlib.md5(password.encode()).hexdigest()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE username = ? AND password_hash = ?',
        (username, password_hash)
    )
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'Invalid credentials'}), 401

    session['user_id'] = user[0]
    session['role'] = user[4]
    return jsonify({'message': 'Login successful', 'user_id': user[0]})


# --- Register ---
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    email = data.get('email', '')

    password_hash = hashlib.md5(password.encode()).hexdigest()

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
            (username, password_hash, email)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

    conn.close()
    return jsonify({'message': 'User created'}), 201
