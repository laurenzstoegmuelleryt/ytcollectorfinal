from telethon import TelegramClient, events
import re
import os
import requests

# Umgebungsvariablen von Render
API_ID = int(os.environ.get("API_ID") or input("API_ID: "))
API_HASH = os.environ.get("API_HASH") or input("API_HASH: ")
SESSION_NAME = os.environ.get("SESSION_NAME", "yt_session")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")  # z. B. "meinChannelName" oder -100123456789
MAKE_WEBHOOK_URL = os.environ.get("MAKE_WEBHOOK_URL")

# Client starten
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Regex für YouTube-Links
yt_pattern = re.compile(r"(https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)[\w\-]+)")

@client.on(events.NewMessage(chats=CHANNEL_USERNAME))
async def handler(event):
    text = event.raw_text
    yt_links = yt_pattern.findall(text)
    if yt_links:
        payload = {"links": yt_links, "message": text}
        requests.post(MAKE_WEBHOOK_URL, json=payload)
        print(f"? YT-Links gesendet: {yt_links}")

print("?? Bot startet...")
client.start()
client.run_until_disconnected()
