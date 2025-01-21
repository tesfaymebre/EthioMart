import os
import pandas as pd
from telethon import TelegramClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")
OUTPUT_DIR = "data/raw/media/"

# Create directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Telegram client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def fetch_messages(channel_list, limit=100):
    data = []
    for channel in channel_list:
        try:
            print(f"Fetching messages from: {channel}")
            async for message in client.iter_messages(channel, limit=limit):
                media_path = None
                # Download media if it exists
                if message.media:
                    media_file = f"{channel}_{message.id}"
                    media_path = os.path.join(OUTPUT_DIR, media_file)
                    await message.download_media(media_path)

                # Add relevant fields to data
                data.append({
                    "Channel Title": message.chat.title if message.chat else None,
                    "Channel Username": channel,
                    "ID": message.id,
                    "Message": message.message,
                    "Date": message.date,
                    "Media Path": media_path
                })
        except Exception as e:
            print(f"Error fetching from {channel}: {e}")
    return data

def load_channels(file_path):
    """Load channel list from CSV"""
    df = pd.read_csv(file_path)
    return df.iloc[:, 0].tolist()

async def main():
    # Load Telegram channels from CSV
    channels = load_channels("data/raw/channels_to_crawl.csv")
    print(f"Loaded {len(channels)} channels.")

    # Fetch messages
    messages = await fetch_messages(channels)

    # Save data to a CSV file
    output_file = os.path.join("data/raw/", "telegram_messages.csv")
    pd.DataFrame(messages).to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
