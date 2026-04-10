import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Your Bot Token
TOKEN = "8323691821:AAHEMw9-MjVxg57n0lSLybjAqUiFC82TbuE"

# yt-dlp configuration for best quality and no watermark
YDL_OPTIONS = {
    'format': 'best',
    'outtmpl': 'downloads/%(id)s.%(ext)s',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hello {user_name}! 🚀\n\n"
        "Send me any Instagram Reels or TikTok link, and I will download it for you without a watermark."
    )

async def handle_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # Check if the link is from Instagram or TikTok
    if any(site in url for site in ["instagram.com", "tiktok.com"]):
        msg = await update.message.reply_text("Processing video... please wait ⏳")
        
        try:
            # Ensure downloads directory exists
            if not os.path.exists('downloads'):
                os.makedirs('downloads')

            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
            # Send the video file
            with open(filename, 'rb') as video:
                await update.message.reply_video(
                    video=video, 
                    caption="Downloaded successfully ✅"
                )
            
            # Clean up files after sending
            os.remove(filename)
            await msg.delete()

        except Exception as e:
            await msg.edit_text(f"Error during download. Make sure the account is Public.\nError: {str(e)}")
    else:
        await update.message.reply_text("Please send a valid TikTok or Instagram link ⚠️")

if __name__ == '__main__':
    # Create directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_download))
    
    print("Bot is running...")
    app.run_polling()
