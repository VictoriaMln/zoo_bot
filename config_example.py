import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

BOT_TOKEN = "YOUR_BOT_TOKEN"
BOT_USERNAME = "YOUR_BOT_NAME"
BOT_LINK = f"https://t.me/{BOT_USERNAME}"
STAFF_CHAT_ID = 123 #id пользователя, которому будут приходить запросы