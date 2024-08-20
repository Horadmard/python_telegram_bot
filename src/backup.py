from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Your bot's API token
API_TOKEN = 'YOUR_API_TOKEN'

# The channel ID or username (e.g., '@yourchannelname' or '-1001234567890')
CHANNEL_ID = '@yourchannelname'

# Create the bot instance
bot = Bot(token=API_TOKEN)

def get_messages(update, context):
    try:
        # Get recent messages from the channel
        updates = bot.get_updates()
        
        # Parse the updates to get messages from the channel
        for update in updates:
            if update.message and update.message.chat.username == CHANNEL_ID:
                print(update.message.text)  # Access the message text
        
        update.message.reply_text("Fetched messages from the channel.")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")


# import json

# def save_messages_to_json(messages, filename='channel_messages.json'):
#     with open(filename, 'w') as file:
#         json.dump(messages, file, indent=4)

# def get_messages(update, context):
#     try:
#         messages = []
#         updates = bot.get_updates()
        
#         for update in updates:
#             if update.message and update.message.chat.username == CHANNEL_ID:
#                 message_data = {
#                     "message_id": update.message.message_id,
#                     "text": update.message.text,
#                     "date": update.message.date.isoformat()
#                 }
#                 messages.append(message_data)
        
#         save_messages_to_json(messages)
#         update.message.reply_text("Messages have been saved to JSON.")
#     except Exception as e:
#         update.message.reply_text(f"Error: {e}")


# Set up the Updater and dispatcher
updater = Updater(API_TOKEN, use_context=True)
dp = updater.dispatcher

# Add a command handler to fetch messages
dp.add_handler(CommandHandler('getmessages', get_messages))

# Start the bot
updater.start_polling()
updater.idle()
