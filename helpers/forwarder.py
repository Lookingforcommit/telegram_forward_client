# (c) @Lookingforcommit
# (c) @AbirHasan2005

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from typing import Set


async def forward_message(client: Client, msg: Message, forward_to_chat_ids: Set[int]) -> Message:
    for chat_id in forward_to_chat_ids:
        try:
            copied_message = await msg.copy(chat_id)
            return copied_message
        except FloodWait as e:
            raise FloodWait(e.value)
        except Exception as e:
            await client.send_message(chat_id="me", text=f"#ERROR: `{e}`\n\nUnable to forward message to `{chat_id}`")
            raise e
