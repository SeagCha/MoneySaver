import asyncio
import json
from telethon import TelegramClient, events

# Загружаем конфигурацию
config = json.load(open('config.json'))

ACCOUNT_SETTINGS = config["ACCOUNT"]
API_ID = ACCOUNT_SETTINGS['API_ID']
API_HASH = ACCOUNT_SETTINGS['API_HASH']
PHONE_NUMBER = ACCOUNT_SETTINGS["PHONE_NUMBER"]
CLOUD_PASSWORD = ACCOUNT_SETTINGS["CLOUD_PASSWORD"]
TELETHON_SESSION = ACCOUNT_SETTINGS["TELETHON_SESSION"]

BOT_SETTINGS = config["BOT_SETTINGS"]
CHANNELS = BOT_SETTINGS["CHANNELS"]
SPECIAL_WORDS = BOT_SETTINGS["SPECIAL_WORDS"]
TARGET_USER = BOT_SETTINGS["TARGET_USER"]

client = TelegramClient(TELETHON_SESSION, API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    # Проверяем, есть ли текст
    message_text = event.message.message
    if not message_text:
        return

    # Если хотя бы одно из "особых" слов встречается в сообщении – пересылаем сообщение
    if any(word in message_text for word in SPECIAL_WORDS):
        for user in TARGET_USER:
            await event.message.forward_to(user)
            print(f"Сообщение переслано с {event.chat_id} на {user}")

async def main():

    await client.start(
        phone=lambda: PHONE_NUMBER,
        password=lambda: CLOUD_PASSWORD
    )
    print("Бот запущен. Ожидание новых сообщений...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())