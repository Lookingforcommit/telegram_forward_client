from pyrogram import Client


async def get_chat_name(client: Client, chat_id: int) -> str:
    try:
        chat = await client.get_chat(chat_id)
        return chat.title or chat.first_name or str(chat_id)
    except Exception:
        return str(chat_id)
