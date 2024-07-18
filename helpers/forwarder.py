# (c) @AbirHasan2005
# (c) @Lookingforcommit

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from typing import Set


async def forward_message(client: Client, msg: Message, forward_as_copy: bool, forward_to_chat_ids: Set[int]):
    for chat_id in forward_to_chat_ids:
        try:
            if forward_as_copy is True:
                await msg.copy(chat_id)
            else:
                await msg.forward(chat_id)
        except FloodWait as e:
            await client.send_message(chat_id="me", text=f"#FloodWait: stopped forwarder for `{e.value}s`!")
            raise e
        except Exception as err:
            await client.send_message(chat_id="me", text=f"#ERROR: `{err}`\n\nUnable to forward message to "
                                      f"`{chat_id}`")
