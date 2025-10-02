import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))

CHANNEL_USERNAME = "@PremiumAccountsBot_Channel"
CHANNEL_URL = f"https://t.me/{CHANNEL_USERNAME[1:]}"

CAPTCHA_QUESTIONS = [
    {"question": "🎯 5 + 3 = ?", "answer": "8"},
    {"question": "🎯 10 - 4 = ?", "answer": "6"}, 
    {"question": "🎯 2 × 3 = ?", "answer": "6"}
]
