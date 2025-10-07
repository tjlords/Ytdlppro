import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from downloader import download_video

# --- Environment Variables from Render ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")       # optional for future Telethon integration
API_HASH = os.getenv("API_HASH")   # optional for future Telethon integration

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a YouTube link (video or playlist), optionally followed by quality (e.g., 1080, 720).\n"
        "Example:\nhttps://youtube.com/watch?v=abcd1234 1080"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split()
    url = parts[0]
    quality = parts[1] if len(parts) > 1 else "best"

    msg = await update.message.reply_text("Downloading video(s)... Please wait!")

    try:
        files = download_video(url, quality=quality)
        if not files:
            await msg.edit_text("No videos were downloaded. Check URL or quality.")
            return

        for fpath in files:
            file_size = os.path.getsize(fpath)
            if file_size < 50 * 1024 * 1024:  # 50 MB limit for send_video
                await update.message.reply_video(video=open(fpath, 'rb'))
            else:
                await update.message.reply_document(document=open(fpath, 'rb'))
            os.remove(fpath)

        await msg.edit_text("All downloads uploaded successfully ✅")

    except Exception as e:
        await msg.edit_text(f"Error: {e}")

# --- Main ---
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
