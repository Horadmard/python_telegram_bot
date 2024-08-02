#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

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

# TOKEN = "7256893867:AAHLJ_ED4uO_8QiNvYb9kKyEbFRlI9ZDaJA"
TOKEN = "7259922195:AAGzmCGq-xhqEnzFffDUlnBomd-oB5YIrXY"

# data = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if not check_user_exists(update.effective_chat.id):
        await update.message.reply_text(
        "شما قبلا ثبت نام کرده اید! ",
        )
        
        return ConversationHandler.END

    user = update.message.from_user
    logger.info("user.id of %s: %s", user.first_name, user.id)

    await update.message.reply_text(
        "🌀 نام و نام‌خانوادگی: ",
    )

    # data.append(update.effective_user.id)
    # print(update.effective_chat.id)

    insert_user_data(update.effective_user.id, ('','','','','','','',''))

    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("name of %s: %s", user.first_name, update.message.text)

    # data.append(update.effective_message.text)
    update_user_data(update.effective_user.id, "name", update.effective_message.text)

    await update.message.reply_text("🌀 سن:")

    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("age of %s: %s", user.first_name, update.message.text)

    # data.append(update.effective_message.text)
    update_user_data(update.effective_user.id, "age", update.effective_message.text)

    await update.message.reply_text(
        "🌀 شماره تلفن همراه:",
        
        )

    return PHONE

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("phone of %s: %s", user.first_name, update.message.text)

    # data.append(update.effective_message.text)
    update_user_data(update.effective_user.id, "phone", update.effective_message.text)

    await update.message.reply_text(
        "🌀 دانشگاه محل تحصیل:\n"
        " - اگه در حال حاضر مشغول به تحصیل نیستید کلیک کنید /skip."
        )

    return UNI


async def uni(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("University of %s: %s", user.first_name, update.message.text)

    # data.append(update.effective_message.text)
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
        " - از این ایمیل برای دریافت کلاس‌های ضبط شده استفاده خواهید کرد.",
        # input_field_placeholder="example@gmail.com"
        )
    
    # data.append('-')
    # data.append('-')
    update_user_data(update.effective_user.id, "uni", '-')
    update_user_data(update.effective_user.id, "stunum", '-')

    return EMAIL

async def stunum(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("Student code of %s: %s", user.first_name, update.message.text)

    # data.append(update.effective_message.text)
    update_user_data(update.effective_user.id, "stunum", update.effective_message.text)

    await update.message.reply_text(
        "🌀 ایمیل شخصی:\n"
        " - از این ایمیل برای دریافت کلاس‌های ضبط شده استفاده خواهید کرد."
        )

    return EMAIL

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("Email of %s: %s", user.first_name, update.message.text)

    # data.append(update.effective_message.text)
    update_user_data(update.effective_user.id, "email", update.effective_message.text)

    # keyboard = [
    #     [
    #         InlineKeyboardButton("بله", callback_data="بله"),
    #         InlineKeyboardButton("خیر", callback_data="خیر"),
    #     ],
        # [InlineKeyboardButton("Option 3", callback_data="3")],
    # ]

    # reply_markup = InlineKeyboardMarkup(keyboard)

    # await update.message.reply_text("Please choose:", reply_markup=reply_markup)

    reply_keyboard = [["بله", "خیر"]]

    await update.message.reply_text(
        "🌀 درخواست گواهی شرکت در دوره رو دارید؟\n"
        " - گواهی از طرف انجمن علمی علوم کامپیوتر یزد صادر میشه و نشون میده شما دوره رو گذروندید.",
        
        # reply_markup=ReplyKeyboardMarkup(
        #     reply_keyboard, one_time_keyboard=True, input_field_placeholder="گواهی شرکت در رویداد؟"
        # ),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="گواهی بدم؟", resize_keyboard=True,
        ),
        # reply_markup=reply_markup,
        )

    return LICENSE

async def license(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    # query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    # await query.answer()
    # await query.edit_message_text(text=f"Selected option: {query.data}")

    user = update.message.from_user
    logger.info("Is he/she whants license? %s: %s", user.first_name, update.message.text)



    # data.append(update.effective_message.text)
    update_user_data(update.effective_user.id, "want_license", update.effective_message.text)

    await update.message.reply_text(
        "🌀 طریقه‌ی آشنایی با رویداد ما:\n"
        " - کانال تلگرامی، اینستاگرم، معرفی دوستان و ...",
        reply_markup=ReplyKeyboardRemove(),
        )

    return REL

async def rel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("%s: %s", user.first_name, update.message.text)

    # data.append(update.effective_message.text)
    update_user_data(update.effective_user.id, "relation", update.effective_message.text)

    await update.message.reply_text(
        "ثبت نام شما با موفقیت انجام شد."
        )

    # print(data)

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
    )

    return ConversationHandler.END

# NAME, AGE, PHONE, UNI, STUNUM, EMAIL, LICENSE, REL

# async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Stores the selected gender and asks for a photo."""
#     user = update.message.from_user
#     logger.info("Gender of %s: %s", user.first_name, update.message.text)
#     await update.message.reply_text(
#         "I see! Please send me a photo of yourself, "
#         "so I know what you look like, or send /skip if you don't want to.",
#         reply_markup=ReplyKeyboardRemove(),
#     )

#     return PHOTO


# async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Stores the photo and asks for a location."""
#     user = update.message.from_user
#     photo_file = await update.message.photo[-1].get_file()
#     await photo_file.download_to_drive("user_photo.jpg")
#     logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
#     await update.message.reply_text(
#         "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
#     )

#     return LOCATION


# async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Skips the photo and asks for a location."""
#     user = update.message.from_user
#     logger.info("User %s did not send a photo.", user.first_name)
#     await update.message.reply_text(
#         "I bet you look great! Now, send me your location please, or send /skip."
#     )

#     return LOCATION


# async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Stores the location and asks for some info about the user."""
#     user = update.message.from_user
#     user_location = update.message.location
#     logger.info(
#         "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
#     )
#     await update.message.reply_text(
#         "Maybe I can visit you sometime! At last, tell me something about yourself."
#     )

#     return BIO


# async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Skips the location and asks for info about the user."""
#     user = update.message.from_user
#     logger.info("User %s did not send a location.", user.first_name)
#     await update.message.reply_text(
#         "You seem a bit paranoid! At last, tell me something about yourself."
#     )

#     return BIO


# async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Stores the info about the user and ends the conversation."""
#     user = update.message.from_user
#     logger.info("Bio of %s: %s", user.first_name, update.message.text)
#     await update.message.reply_text("Thank you! I hope we can talk again some day.")

#     return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
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
            # UNI: [MessageHandler(filters.TEXT, uni), CommandHandler("skip", skip_uni)],
            STUNUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, stunum)],
            EMAIL: [MessageHandler(filters.Regex(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email)],
            # EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            LICENSE: [MessageHandler(filters.Regex("^(بله|خیر)$"), license)],
            REL: [MessageHandler(filters.TEXT & ~filters.COMMAND, rel)],

            # GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
            # PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
            # LOCATION: [
            #     MessageHandler(filters.LOCATION, location),
            #     CommandHandler("skip", skip_location),
            # ],
            # BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
# NAME, AGE, PHONE, UNI, STUNUM, EMAIL, LICENSE, REL
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()