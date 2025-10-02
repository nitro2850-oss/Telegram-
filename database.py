import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            subscribed BOOLEAN DEFAULT FALSE,
            passed_captcha BOOLEAN DEFAULT FALSE,
            completed_onboarding BOOLEAN DEFAULT FALSE,
            created_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT OR IGNORE INTO users (user_id, username, created_at) VALUES (?, ?, ?)',
        (user_id, username, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_subscription(user_id, subscribed):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET subscribed = ? WHERE user_id = ?', (subscribed, user_id))
    conn.commit()
    conn.close()

def update_user_captcha(user_id, passed):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET passed_captcha = ? WHERE user_id = ?', (passed, user_id))
    conn.commit()
    conn.close()

def update_user_onboarding(user_id, completed):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET completed_onboarding = ? WHERE user_id = ?', (completed, user_id))
    conn.commit()
    conn.close()
