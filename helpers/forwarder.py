# (c) @AbirHasan2005
# (c) @Lookingforcommit

import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from typing import List

from helpers.filters import FilterMessage


async def ForwardMessage(client: Client, msg: Message, forward_as_copy: bool, forward_to_chat_ids: List[int],
                         forward_filters: List[str]):
    try:
        ## --- Check 1 --- ##
        can_forward = await FilterMessage(msg, forward_filters)
        if can_forward == 400:
            return 400
        ## --- Check 2 --- ##
        for i in range(len(forward_to_chat_ids)):
            try:
                if forward_as_copy is True:
                    await msg.copy(forward_to_chat_ids[i])
                else:
                    await msg.forward(forward_to_chat_ids[i])
            except FloodWait as e:
                await client.send_message(chat_id="me", text=f"#FloodWait: Stopped Forwarder for `{e.value}s`!")
                await asyncio.sleep(e.value)
                await ForwardMessage(client, msg, forward_as_copy, forward_to_chat_ids, forward_filters)
            except Exception as err:
                await client.send_message(chat_id="me", text=f"#ERROR: `{err}`\n\nUnable to Forward Message to "
                                                             f"`{str(forward_to_chat_ids[i])}`")
    except Exception as err:
        await client.send_message(chat_id="me", text=f"#ERROR: `{err}`")
