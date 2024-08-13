from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from typing import Set
import asyncio


async def forward_message(client: Client, msg: Message, forward_as_copy: bool, forward_to_chat_ids: Set[int]):
    for chat_id in forward_to_chat_ids:
        try:
            if forward_as_copy is True:
                await msg.copy(chat_id)
            else:
                await msg.forward(chat_id)
        except FloodWait as e:
            print(f"FloodWait: {e.value} seconds")
            await asyncio.sleep(e.value)
        except Exception as err:
            print(f"Error forwarding message: {str(err)}")
            await client.send_message(chat_id="me", text=f"#ERROR: `{str(err)}`\n\nUnable to forward message to "
                                                         f"`{chat_id}`")
