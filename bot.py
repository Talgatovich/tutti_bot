import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

updater = Updater(token=bot_token)
url = "http://www.notomania.ru/noty_pesni.php?n=1641#"


def say_hi(update, context):
    # Получаем информацию о чате, из которого пришло сообщение,
    # и сохраняем в переменную chat
    chat = update.effective_chat
    # print(chat)
    print(update)
    # В ответ на любое текстовое сообщение
    # будет отправлено 'Привет, я KittyBot!'
    context.bot.send_message(
        chat_id=chat.id, text=f"Привет, {chat.first_name}!"
    )


def wake_up(update, context):
    # В ответ на команду /start
    # будет отправлено сообщение 'Спасибо, что включили меня'
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([["Начать"]], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f"Спасибо, что включили меня, {chat.first_name}",
        reply_markup=button,
    )


# Регистрируется обработчик MessageHandler;
# из всех полученных сообщений он будет выбирать только текстовые сообщения
# и передавать их в функцию say_hi()
updater.dispatcher.add_handler(CommandHandler("start", wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))


# Метод start_polling() запускает процесс polling,
# приложение начнёт отправлять регулярные запросы для получения обновлений.
updater.start_polling()
# Бот будет работать до тех пор, пока не нажмете Ctrl-C
updater.idle()
