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
        file.write("Đây là nội dung của file được tạo bởi bot.")
    await update.message.reply_text("File đã được tạo thành công!")

async def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(CommandHandler("taixiu", taixiu))
    app.add_handler(CommandHandler("createfile", create_file))
    
    print("Bot đang chạy...")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if str(e) != "Event loop is closed":
            raise
