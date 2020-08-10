import os
import logging
import pytesseract

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi!. Send me photo to extract text. "Work only on english language"')




def ocr(update, context):
    chat_id = update.message.chat.id
    file_id = update.message.photo[-1].file_id
    file_name = file_id + ".png"
    picture = context.bot.get_file(file_id).download('./data/{}'.format(file_name))
    try:
        text = pytesseract.image_to_string('./data/{}'.format(file_name))
        if text == "":
            if update.message.chat.type == "supergroup":
                return # won't show error messages in groups
            else:
                text = "sorry, unable to extract text from your image."
    except:
        text = "sorry, an error has occured while processing your image."
    context.bot.send_message(chat_id=chat_id, text=text)



def help(update, context):
    update.message.reply_text('Help!. You can contact me @lisaamane')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    try:
        TOKEN = '1313618030:AAFf2bcFIbw4h_WGIwn7gb-WcPteOdzDWjA'
    except IndexError:
        TOKEN = os.environ.get("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, ocr))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info("Ready to rock..!")
    updater.idle()


if __name__ == '__main__':
    main()