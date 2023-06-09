import youtube_dl
from telegram.ext import Updater, CommandHandler

# Telegram bot token
TOKEN = "5782499781:AAGJRQaLbtSDd6yGb1dPEfAz6h1SFzqrhnU"

# Function to handle the /download command
def download_handler(update, context):
    # Get the video URL from the command arguments
    video_url = " ".join(context.args)

    # Download the Facebook video using youtube_dl
    ydl_opts = {
        'outtmpl': 'video.mp4',  # Output filename
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Send the video file to the user
    context.bot.send_video(chat_id=update.message.chat_id, video=open('video.mp4', 'rb'))

# Create the Telegram bot and add the download command handler
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("download", download_handler))

# Start the bot
updater.start_polling()
