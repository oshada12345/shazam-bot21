import requests
from telegram.ext import Updater, CommandHandler
from telegram import InputMediaAudio, InputMediaDocument

# Telegram bot token
TOKEN = "5782499781:AAGJRQaLbtSDd6yGb1dPEfAz6h1SFzqrhnU"

# Genius API token
GENIUS_TOKEN = "wTwRe4nkGkFSVZBDXKjQH4Cxd3Y4b4ik_LABD44N8KbezmO-_pV5svgUqdUoaxBg"

# Function to handle the /song command
def song_handler(update, context):
    # Get the song name from the command arguments
    song_name = " ".join(context.args)
    
    # Search for the song on Genius
    headers = {'Authorization': f'Bearer {GENIUS_TOKEN}'}
    search_url = f"https://api.genius.com/search?q={song_name}"
    response = requests.get(search_url, headers=headers).json()
    
    # Get the first search result
    if 'response' in response and 'hits' in response['response']:
        hits = response['response']['hits']
        if hits:
            song_data = hits[0]['result']
            song_title = song_data['title']
            song_artist = song_data['primary_artist']['name']
            song_lyrics_url = song_data['url']
            song_audio_url = song_data['media'][0]['url']
            
            # Send the song details and lyrics
            update.message.reply_text(f"Title: {song_title}\nArtist: {song_artist}")
            update.message.reply_text(f"Lyrics: {song_lyrics_url}")
            
            # Send the song audio or video file
            if song_audio_url.endswith('.mp3'):
                context.bot.send_audio(chat_id=update.message.chat_id, audio=song_audio_url)
            else:
                context.bot.send_document(chat_id=update.message.chat_id, document=song_audio_url)
        else:
            update.message.reply_text("Song not found!")
    else:
        update.message.reply_text("Failed to search for the song!")

# Create the Telegram bot and add the song command handler
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("song", song_handler))

# Start the bot
updater.start_polling()
