import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import my_parser

TEXT = "Напишите фамилию композитора и название произведения через дефис"

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
updater = Updater(token=bot_token)


def wake_up(update, context):
    chat = update.effective_chat
    name = chat.first_name
    button = ReplyKeyboardMarkup([["start"], ["search"]], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f"Здравствуйте, {name}! Спасибо, что включили меня! {TEXT}",
        reply_markup=button,
    )


def search(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=TEXT,
    )


def ask_me(update, context):
    chat = update.effective_chat
    search = update["message"]["text"].split("-")

    try:
        author = search[0].strip()
        title = search[1].strip()
    except IndexError:
        context.bot.send_message(
            chat_id=chat.id,
            text=TEXT,
        )
        return

    try:
        data = my_parser.main_page()
        compositions_url = my_parser.search_author(author, data)
        link = my_parser.search_composition(compositions_url, title)
        dowload_link = my_parser.download_notes(link)
    except Exception:
        context.bot.send_message(
            chat_id=chat.id, text=f"Что-то пошло не так! :(  {TEXT}"
        )
    try:
        context.bot.send_document(chat_id=chat.id, document=dowload_link)
    except Exception:
        context.bot.send_message(chat_id=chat.id, text=dowload_link)


if __name__ == "__main__":
    updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    updater.dispatcher.add_handler(CommandHandler("search", search))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, ask_me))
    updater.start_polling()
    updater.idle()
