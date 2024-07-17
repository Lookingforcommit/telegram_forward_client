# (c) @AbirHasan2005
# (c) @Lookingforcommit

from typing import List
from pyrogram.types import Message


async def FilterMessage(message: Message, forward_filters: List[str]):
    if (message.forward_from or message.forward_from_chat) and ("forwarded" not in forward_filters):
        return 400
    if (len(forward_filters) == 0) or ((message.video and ("video" in forward_filters)) or (message.document and ("document" in forward_filters)) or (message.photo and ("photo" in forward_filters)) or (message.audio and ("audio" in forward_filters)) or (message.text and ("text" in forward_filters)) or (message.animation and ("gif" in forward_filters)) or (message.poll and ("poll" in forward_filters)) or (message.sticker and ("sticker" in forward_filters))):
        return 200
    else:
        return 400
