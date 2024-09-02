# (c) @Lookingforcommit
# (c) @synthimental

from pyrogram import Client
from pyrogram.types import Message

from scenarios.scenarios_classes.base import BaseScenario


class SampleScenario(BaseScenario):
    DESCRIPTION = ("Sample scenario for testing purposes. "
                   "It changes message text to [new_text]")
    ARGUMENTS_CONVERSION_FUNCTIONS = {
        "new_text": str
    }
    ARGUMENTS_INFO = {
        "new_text": "String that will replace the text in processed messages"
    }

    async def apply(self, client: Client, message: Message, **kwargs) -> Message:
        if message.text is not None:
            new = await message.edit_text(kwargs["new_text"])
            return new
        if message.caption is not None:
            new = await message.edit_caption(kwargs["new_text"])
            return new
