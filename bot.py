import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from downloader import download_video

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Start command
def start(update, context):
    update.message.reply_text("Hello! Send me a YouTube link and quality (like '720') to download.")

# Help command
def help_command(update, context):
    update.message.reply_text("Send a YouTube video or playlist link followed by desired quality (like 1080, 720).")

# Handle messages (YouTube links)
def handle_message(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    if text.startswith("https://") or text.startswith("http://"):
        parts = text.split()
        url = parts[0]
        quality = parts[1] if len(parts) > 1 else "bestvideo+bestaudio"
        update.message.reply_text(f"Downloading {url} at quality {quality}...")
        try:
            file_path = download_video(url, quality)
            update.message.reply_document(open(file_path, "rb"))
        except Exception as e:
            update.message.reply_text(f"Error: {str(e)}")
    else:
        update.message.reply_text("Send a valid YouTube URL.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
