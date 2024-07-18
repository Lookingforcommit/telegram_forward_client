# (c) @AbirHasan2005
# (c) @Lookingforcommit

import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from typing import List, Set


async def ForwardMessage(client: Client, msg: Message, forward_as_copy: bool, forward_to_chat_ids: Set[int],
                         forward_filters: List[str]):
    try:
        for chat_id in forward_to_chat_ids:
            try:
                if forward_as_copy is True:
                    await msg.copy(chat_id)
                else:
                    await msg.forward(chat_id)
            except FloodWait as e:
                await client.send_message(chat_id="me", text=f"#FloodWait: Stopped Forwarder for `{e.value}s`!")
                await asyncio.sleep(e.value)
                await ForwardMessage(client, msg, forward_as_copy, forward_to_chat_ids, forward_filters)
            except Exception as err:
                await client.send_message(chat_id="me", text=f"#ERROR: `{err}`\n\nUnable to Forward Message to "
                                                             f"`{chat_id}`")
    except Exception as err:
        await client.send_message(chat_id="me", text=f"#ERROR: `{err}`")
