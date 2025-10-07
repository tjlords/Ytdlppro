import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from downloader import download_video

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send a YouTube link and optional quality (like '720').")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a YouTube video or playlist link followed by desired quality (like 1080, 720).")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("https://") or text.startswith("http://"):
        parts = text.split()
        url = parts[0]
        quality = parts[1] if len(parts) > 1 else "bestvideo+bestaudio"
        await update.message.reply_text(f"Downloading {url} at quality {quality}...")
        try:
            file_paths = download_video(url, quality)
            if not isinstance(file_paths, list):
                file_paths = [file_paths]
            for file_path in file_paths:
                await update.message.reply_document(open(file_path, "rb"))
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    else:
        await update.message.reply_text("Send a valid YouTube URL.")

async def main():
    # Use ApplicationBuilder, not Updater
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
