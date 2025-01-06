

import os, re, json, logging
from db import *
from search import *


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


def load_config(filename='config.json'):
    # Construct the path to the config file in the parent directory
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the current file's directory
    config_path = os.path.join(parent_directory, filename)  # Create the path to the config file

    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

# Load the configuration
config = load_config()



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

STDID = range(1)

TOKEN = config['TOKEN']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("user.id of %s: %s", user.first_name, user.id)

    if check_user_exists(update.effective_chat.id):

        record = search_in_excel(get_element(update.effective_user.id, 'stu_num'))

        if record is not None and not record.empty:
            for index, (_, r) in enumerate(record.iterrows(), start=1):
                await update.message.reply_text(
                    f"به این زودی یادت رفت؟!\nکد تخفیف شما:\n{r['کد تخفیف']}",
                )
        
        return ConversationHandler.END
    
    elif not check_user_exists(update.effective_chat.id):
        insert_user_data(update.effective_user.id, (''))
        await update.message.reply_text(
            "سلام\n🌀 کد دانشجوییتو بده ببینم:",
        )

    return STDID


async def getstdid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("name of %s: %s", user.first_name, update.message.text)

    update_user_data(update.effective_user.id, 'stu_num', convert_numbers(update.message.text))
    record = search_in_excel(get_element(update.effective_user.id, 'stu_num'))

    if record is not None and not record.empty:
        for index, (_, r) in enumerate(record.iterrows(), start=1):
            await context.bot.send_message(
                chat_id=user.id,
                text=f"بفرمایید {r['نام']} "
                    f"{r['نام‌خانوادگی']} "
                    f"عزیز:\n{r['کد تخفیف']}"
            )


    else:
        await context.bot.send_message(
            chat_id=user.id,
            text="همچین کسی نداریم!\nدوباره امتحان کن /start",
            reply_markup=ReplyKeyboardRemove()
        )
        print(record)
        delete_user_by_id(user.id)
        return ConversationHandler.END
    
    return ConversationHandler.END 

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the registration.", user.first_name)
    await update.message.reply_text(
        "اطلاعاتت هوتوتو؛\n"
        "/start برای از سر گیری فرآیند.",
        reply_markup=ReplyKeyboardRemove(),
    )

    delete_user_by_id(update.effective_user.id)
    return ConversationHandler.END

async def show_all_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("User %s Show all Data.", user.first_name)

    records = show_excel()
    for index, (_, r) in enumerate(records.iterrows(), start=1):
        await update.message.reply_text(
            f"{r['ردیف']}- {r['نام']} {r['نام‌خانوادگی']}, {r['شماره دانشجویی']}, {r['کد تخفیف']}",
            reply_markup=ReplyKeyboardRemove(),
        )
        # print(f"{r['ردیف']}- {r['نام']} {r['نام‌خانوادگی']}, {r['شماره دانشجویی']}, {r['کد تخفیف']}")


    # delete_user_by_id(update.effective_user.id)
    return ConversationHandler.END

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("User %s wants help.", user.first_name)
    await update.message.reply_text(
        "هر سوال یا مشکلی داری، میتونی از این آیدی بپرسی:\n\n"
        "@cs_yazd_admin"
    )
    return ConversationHandler.END


def main() -> None:

    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # YN: [MessageHandler(filters.TEXT & ~filters.COMMAND, yesorno)],
            STDID: [MessageHandler(filters.TEXT & ~filters.COMMAND, getstdid)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('show', show_all_data))
    application.add_handler(CommandHandler('cankel', cancel))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":

    main()