from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pydub import AudioSegment
import os

# Replace with your bot token
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Function to change pitch of the voice
def change_pitch(input_file, output_file, semitones=4):
    sound = AudioSegment.from_file(input_file)
    octaves = semitones / 12.0
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

    # Change the pitch
    pitched_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    pitched_sound = pitched_sound.set_frame_rate(44100)
    pitched_sound.export(output_file, format="wav")
    print(f"Modified voice saved as {output_file}")

# /start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me a voice file, and I will modify its pitch to sound like a girl.")

# Voice message handler
def handle_voice(update: Update, context: CallbackContext) -> None:
    voice_file = update.message.voice.get_file()
    input_file = "input_voice.ogg"
    output_file = "modified_voice.wav"

    try:
        # Download the voice file
        voice_file.download(input_file)

        # Convert the pitch
        change_pitch(input_file, output_file, semitones=4)

        # Send the modified voice back
        with open(output_file, "rb") as audio:
            update.message.reply_audio(audio, caption="Here's your modified voice!")

        # Clean up temporary files
        os.remove(input_file)
        os.remove(output_file)

    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

# Main function to set up the bot
def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.voice, handle_voice))

    # Start the bot
    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
