import os
import random
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = os.getenv("BOT_TOKEN")  # Lấy token từ biến môi trường

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Chào bạn! Tôi là bot Telegram chạy trên Render.")

async def echo(update: Update, context: CallbackContext):
    await update.message.reply_text(update.message.text)

async def taixiu(update: Update, context: CallbackContext):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice3 = random.randint(1, 6)
    total = dice1 + dice2 + dice3
    result = "Tài" if total >= 11 else "Xỉu"
    await update.message.reply_text(f"🎲 Xúc xắc: {dice1} - {dice2} - {dice3}\nTổng: {total} => {result}")

async def create_file(update: Update, context: CallbackContext):
    file_name = "bot_output.txt"
    with open(file_name, "w") as file:
        file.write("Đây là file được tạo bởi bot Telegram.\n")
    await update.message.reply_document(document=open(file_name, "rb"))
    os.remove(file_name)

async def check_uid_ff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args  # Lấy danh sách các đối số
    if not args:
        await update.message.reply_text("Vui lòng nhập UID Free Fire! Ví dụ: /checkuid 123456789")
        return
    uid = context.args[0]
    url = f"http://minhnguyen3004.x10.mx/checkuid?uid={uid}"  # API giả định, cần thay bằng API thật
    try:
        response = requests.get(url)
        data = response.json()
        if "error" in data:
            await update.message.reply_text("UID không hợp lệ hoặc không tồn tại.")
        else:
            await update.message.reply_text(f"Thông tin UID {uid}: {data}")
    except Exception as e:
        await update.message.reply_text("Lỗi khi kiểm tra UID. Vui lòng thử lại sau!")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("taixiu", taixiu))
    app.add_handler(CommandHandler("checkuid", check_uid_ff))
    app.add_handler(CommandHandler("createfile", create_file))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("Bot đã khởi chạy...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
