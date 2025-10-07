import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from downloader import download_video

# --- Environment Variables ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")       # optional for Telethon/advanced use
API_HASH = os.getenv("API_HASH")   # optional for Telethon/advanced use

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a YouTube link, and I will download and upload it!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("Downloading video... This may take a while.")

    try:
        filepath = download_video(url)
        file_size = os.path.getsize(filepath)

        # Upload logic based on file size
        if file_size < 50 * 1024 * 1024:  # 50 MB limit for send_video
            await msg.edit_text("Uploading video...")
            await update.message.reply_video(video=open(filepath, 'rb'))
        else:
            await msg.edit_text("Uploading large video as document...")
            await update.message.reply_document(document=open(filepath, 'rb'))

        os.remove(filepath)  # Clean up
        await msg.edit_text("Upload complete ✅")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# --- Main ---
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
