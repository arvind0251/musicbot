import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from pydub import AudioSegment

# Get the bot token from environment variables or .env file
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # or hardcode the token if testing locally

def modify_voice(input_file, output_file, pitch_shift=3):
    """Modify the pitch of the audio."""
    audio = AudioSegment.from_file(input_file)
    shifted_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * (2.0 ** (pitch_shift / 12.0)))
    })
    shifted_audio = shifted_audio.set_frame_rate(audio.frame_rate)
    shifted_audio.export(output_file, format="wav")
    return output_file

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message."""
    await update.message.reply_text("Welcome! Send me an audio file, and I'll modify its pitch for you.")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the received audio file and modify its pitch."""
    if update.message.voice or update.message.audio:
        # Download the audio file
        file = await context.bot.get_file(update.message.voice.file_id if update.message.voice else update.message.audio.file_id)
        input_file = "input_audio.ogg"
        await file.download_to_drive(input_file)

        # Modify the audio
        output_file = "modified_audio.wav"
        modify_voice(input_file, output_file)

        # Send the modified audio back to the user
        await update.message.reply_audio(audio=InputFile(output_file))

        # Clean up files
        os.remove(input_file)
        os.remove(output_file)
    else:
        await update.message.reply_text("Please send an audio or voice file.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))

    print("Bot is running...")
    app.run_polling()
