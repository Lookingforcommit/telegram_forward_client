# (c) @Lookingforcommit

from pyrogram import Client
from typing import Dict, Any


async def get_chat_name(client: Client, chat_id: int) -> str:
    try:
        chat = await client.get_chat(chat_id)
        return chat.title or chat.first_name or str(chat_id)
    except Exception:
        return str(chat_id)


def load_dict_with_int_keys(data, dct_name: str) -> Dict[int, Any]:
    dct = data.get(dct_name, {})
    if dct:
        dct = {int(key): dct[key] for key in dct}
    return dct
