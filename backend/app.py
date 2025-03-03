# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS challenges (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT, 
                        description TEXT,
                        solution TEXT)''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    try:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/challenge/sql_injection', methods=['POST'])
def sql_injection():
    data = request.get_json()
    user_input = data['input']
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        if result:
            return jsonify({'message': 'Success! You exploited the SQL injection!', 'data': result})
        else:
            return jsonify({'message': 'No results found. Try again!'}), 400
    except Exception as e:
        return jsonify({'error': 'SQL error, possibly prevented!'}), 400

@app.route('/challenges', methods=['GET'])
def get_challenges():
    challenges = [
        {"id": 1, "name": "SQL Injection", "description": "Exploit a vulnerable login form."},
        {"id": 2, "name": "XSS Attack", "description": "Inject malicious JavaScript into a webpage."}
    ]
    return jsonify(challenges)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)