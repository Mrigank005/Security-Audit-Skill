import sqlite3
import hashlib
import yaml
import os
from flask import Blueprint, request, jsonify, send_file, abort

users_bp = Blueprint('users', __name__)

DATABASE = 'app.db'


def get_db():
    return sqlite3.connect(DATABASE)


# --- Get user by ID ---
@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db()
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user[0], 'username': user[1], 'email': user[3]})


# --- Search users ---
@users_bp.route('/users/search', methods=['GET'])
def search_users():
    term = request.args.get('q', '')
    conn = get_db()
    cursor = conn.cursor()

    query = f"SELECT id, username, email FROM users WHERE username LIKE '%{term}%'"
    cursor.execute(query)

    users = cursor.fetchall()
    conn.close()
    return jsonify([{'id': u[0], 'username': u[1], 'email': u[2]} for u in users])


# --- Import user config (YAML) ---
@users_bp.route('/users/import', methods=['POST'])
def import_config():
    data = request.get_data(as_text=True)

    config = yaml.load(data, Loader=yaml.FullLoader)

    return jsonify({'message': 'Config imported', 'keys': list(config.keys())})


# --- Download file ---
@users_bp.route('/files/download', methods=['GET'])
def download_file():
    filename = request.args.get('name', '')

    filepath = os.path.join('/var/uploads', filename)

    if not os.path.exists(filepath):
        abort(404)

    return send_file(filepath)
