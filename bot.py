import os
import telebot
import sqlite3
from flask import Flask
from threading import Thread

# Lấy token từ biến môi trường để bảo mật
TOKEN = os.getenv("BOT_TOKEN", "")
if not TOKEN:
    raise ValueError("Vui lòng đặt biến môi trường BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot đang chạy!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Chạy Flask trên một luồng riêng để không chặn bot
Thread(target=run_flask, daemon=True).start()

# Hàm xử lý tin nhắn
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Chào mừng bạn! Bot đang hoạt động.")

# Khởi chạy bot
if __name__ == "__main__":
    print("Bot đang chạy...")
    bot.infinity_polling()
