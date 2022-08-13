# tutti_bot
Бот в telegram, который предоставляет файл с нотами либо ссылку на них по запросу пользователя

#### Запуск проекта на локальной машине.

Перед запуском нужно будет создать бота в Telegram через [BotFather](https://t.me/BotFather) и получить токен, а так же узнать свой id в Telegram через [userinfobot](https://t.me/userinfobot)

- Склонировать проект 
```
git clone git@github.com:Talgatovich/tutti_bot.git
```
- Установить  и активировать виртуальное окружение
```
python -m venv venv
```
```
source venv/Scripts/activate
```
- Установить зависимости
```
pip install -r requirements.txt
```
- Создать файл .env и прописать в ней переменные:
```
BOT_TOKEN - токен созданного бота
```
- Запустить файл bot.py
