from pyrogram.types import Message


def delete_media(message: Message):
    if message.media:
        message.media = None


try:
    delete_media(message)
except Exception as e:
    print(f"An error occurred in the scenario: {str(e)}")
