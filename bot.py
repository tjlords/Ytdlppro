import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from downloader import download_video

# Read Telegram credentials from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")       # For Telethon/advanced use if needed
API_HASH = os.getenv("API_HASH")   # For Telethon/advanced use if needed

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a YouTube link, and I will download and upload it!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("Downloading video... This may take a while.")

    try:
        filepath = download_video(url)
        file_size = os.path.getsize(filepath)

        # Choose upload method based on size
        if file_size < 50 * 1024 * 1024:  # 50 MB
            await msg.edit_text("Uploading video...")
            await update.message.reply_video(video=open(filepath, 'rb'))
        else:
            await msg.edit_text("Uploading large video as document...")
            await update.message.reply_document(document=open(filepath, 'rb'))

        os.remove(filepath)  # Clean up downloaded file
        await msg.edit_text("Upload complete ✅")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Build and run bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
