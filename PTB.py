
from database import *

import logging
from typing import Optional, Tuple

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

NAME, AGE, PHONE, UNI, STUNUM, EMAIL, LICENSE, REL = range(8)

# TOKEN = '...'



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if check_user_exists(update.effective_chat.id):
        await update.message.reply_text(
        "شما قبلا ثبت‌نام کردید!!!",
        )
        
        return ConversationHandler.END

    user = update.message.from_user
    logger.info("user.id of %s: %s", user.first_name, user.id)

    await update.message.reply_text(
        "🌀 نام و نام‌خانوادگی: ",
    )

    insert_user_data(update.effective_user.id, ('','','','','','','',''))

    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("name of %s: %s", user.first_name, update.message.text)

    update_user_data(update.effective_user.id, "name", update.effective_message.text)

    await update.message.reply_text("🌀 سن:")

    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("age of %s: %s", user.first_name, update.message.text)

    update_user_data(update.effective_user.id, "age", update.effective_message.text)

    await update.message.reply_text(
        "🌀 شماره تلفن همراه:",
        
        )

    return PHONE

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("phone of %s: %s", user.first_name, update.message.text)

    update_user_data(update.effective_user.id, "phone", update.effective_message.text)

    await update.message.reply_text(
        "🌀 دانشگاه محل تحصیل: \n"
        "_  \- اگه در حال حاضر مشغول به تحصیل نیستی کلیک کن /skip _",
        parse_mode='MarkdownV2'
        )

    return UNI


async def uni(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("University of %s: %s", user.first_name, update.message.text)

    update_user_data(update.effective_user.id, "uni", update.effective_message.text)

    await update.message.reply_text(
        "🌀 شماره دانشجویی:"
        )

    return STUNUM

async def skip_uni(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)

    await update.message.reply_text(
        "🌀 ایمیل شخصی:\n"
        "_  \- از این ایمیل برای دریافت کلاس‌های ضبط شده استفاده خواهید کرد\. _",
        parse_mode='MarkdownV2',
        )

    update_user_data(update.effective_user.id, "uni", '-')
    update_user_data(update.effective_user.id, "stunum", '-')

    return EMAIL

async def stunum(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("Student code of %s: %s", user.first_name, update.message.text)
    update_user_data(update.effective_user.id, "stunum", update.effective_message.text)

    await update.message.reply_text(
        "🌀 ایمیل شخصی:\n"
        "_  \- از این ایمیل برای دریافت کلاس‌های ضبط شده استفاده خواهید کرد\. _",
        parse_mode='MarkdownV2',
        )

    return EMAIL

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("Email of %s: %s", user.first_name, update.message.text)
    update_user_data(update.effective_user.id, "email", update.effective_message.text)

    reply_keyboard = [["بله", "خیر"]]

    await update.message.reply_text(

        "🌀 درخواست گواهی شرکت در دوره رو دارید؟\n"
        "_  \- گواهی از طرف انجمن علمی علوم کامپیوتر یزد صادر میشه و نشون میده شما دوره رو گذروندید\. _",
        parse_mode='MarkdownV2',

        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="گواهی بدم؟", resize_keyboard=True,
        ),

        )

    return LICENSE

async def license(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("Is he/she whants license? %s: %s", user.first_name, update.message.text)
    update_user_data(update.effective_user.id, "want_license", update.effective_message.text)

    await update.message.reply_text(
        "🌀 طریقه‌ی آشنایی با رویداد ما:\n"
        "_  \- کانال تلگرامی، اینستاگرم، معرفی دوستان و \.\.\. _",
        parse_mode='MarkdownV2',
        reply_markup=ReplyKeyboardRemove(),
        )

    return REL


async def rel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("%s: %s", user.first_name, update.message.text)

    update_user_data(update.effective_user.id, "relation", update.effective_message.text)

    await update.message.reply_text(
        "ثبت نام شما با *موفقیت* انجام شد\.",
        parse_mode='MarkdownV2'
        )

    txt = f"""

🔗 فرم ثبت نام دوره پایتون

🌀 نام و نام‌خانوادگی: {get_element(update.effective_user.id, 'name')}

🌀 سن: {get_element(update.effective_user.id, 'age')}

🌀 شماره تلفن همراه: {get_element(update.effective_user.id, 'phone')}

🌀 دانشگاه محل تحصیل: {get_element(update.effective_user.id, 'uni')}
- اگه در حال حاضر مشغول به تحصیل نیستید این بخش و بخش بعدی رو خالی بزارید.

🌀 شماره دانشجویی: {get_element(update.effective_user.id, 'stunum')}

🌀 ایمیل شخصی: {get_element(update.effective_user.id, 'email')}
- از این ایمیل برای دریافت کلاس‌های ضبط شده استفاده خواهید کرد.

🌀 درخواست گواهی شرکت در دوره رو دارید؟ {get_element(update.effective_user.id, 'want_license')}
- گواهی از طرف انجمن علمی علوم کامپیوتر یزد صادر میشه و نشون میده شما دوره رو گذروندید.

🌀 طریقه‌ی آشنایی با رویداد ما: {get_element(update.effective_user.id, 'relation')}
- کانال تلگرامی، اینستاگرم، معرفی دوستان و ...


"""
    await context.bot.send_message(
        chat_id='@python_database',
        text=txt,
        # parse_mode='MarkdownV2',
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the registration.", user.first_name)
    await update.message.reply_text(
        # "ثبت‌نام هوتوتو ..."
        "ثبت‌نام لغو شد؛\n"
        "اگه خواستی از اول ثبت‌نام کنی کلیک کن /start",
        reply_markup=ReplyKeyboardRemove(),
    )

    delete_user_by_id(update.effective_user.id)

    # data.clear()

    return ConversationHandler.END


def main() -> None:

    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
            UNI: [MessageHandler(filters.TEXT & ~filters.COMMAND, uni), CommandHandler("skip", skip_uni)],
            STUNUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, stunum)],
            EMAIL: [MessageHandler(filters.Regex(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email)],
            LICENSE: [MessageHandler(filters.Regex("^(بله|خیر)$"), license)],
            REL: [MessageHandler(filters.TEXT & ~filters.COMMAND, rel)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    
    application.add_handler(CommandHandler('cancel', cancel))

    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()