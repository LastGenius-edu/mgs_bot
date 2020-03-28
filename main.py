#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import os
from random import randint

# imports for image manipulation
from uuid import uuid4
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# imports for telegram bot code
from telegram import InlineQueryResultPhoto, InlineQueryResultArticle ,ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi! I'm an inline bot, just type some text into "
                              "a box after calling @cropped_mgs_bot and I will send you an image")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Do you really need help? If yeah, just call the suicide prevention hotline'
                              ' for your country at: https://www.suicidestop.com/call_a_hotline.html')


def generate_meme(text):
    img_number = randint(1, 10)
    print(f"chose picture #{img_number}")
    img = Image.open(os.path.join("images", f"img{img_number}.png"))
    draw = ImageDraw.Draw(img)

    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype(os.path.join("images", "impact.ttf"), 12)

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((0, 0), text, (255, 255, 255), font=font)
    print(f"edited image with text '{text}', height: {img.height}, width: {img.width}")
    path = "output/img.png"
    img.save(path)
    print(f"saved image by path '{path}'")

    return img.height, img.width


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    print(f"received query='{query}'")
    size = generate_meme(query)
    results = [
        InlineQueryResultPhoto(
            type='photo',
            id="1",
            title="Picture",
            photo_url="https://github.com/LastGenius-edu/mgs_bot/blob/master/output/img.png",
            thumb_url="https://github.com/LastGenius-edu/mgs_bot/blob/master/output/img.png",
            photo_height=size[0],
            photo_width=size[1],
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)
    print("updated message")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    token = os.environ['TELEGRAM_TOKEN']
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
