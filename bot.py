import os
import telebot
import flask

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Vui lòng đặt biến môi trường BOT_TOKEN!")

bot = telebot.TeleBot(TOKEN)
app = flask.Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = flask.request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def webhook():
    return "Bot đang chạy Webhook!", 200

def set_webhook():
    webhook_url = f"https://checkfreefire.onrender.com/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    print(f"Webhook đã được thiết lập tại {webhook_url}")

if __name__ == '__main__':
    set_webhook()
    app.run(host='0.0.0.0', port=8080)
