# (c) @Lookingforcommit

from pyrogram import Client
from pyrogram.types import Message
from copy import copy

from scenarios.scenarios_classes.base import BaseScenario


class TextInsertionScenario(BaseScenario):
    DESCRIPTION = "Scenario that inserts text to the end of your message."
    ARGUMENTS_CONVERSION_FUNCTIONS = {
        "insertion_list": list,
        "separator": str
    }
    ARGUMENTS_INFO = {
        "insertion_list": "List of format [str1, str2, ...]\n"
                          "It is possible to use markdown/html formatting in strings",
        "separator": "Symbol that separates inserted strings"
    }

    async def apply(self, client: Client, message: Message, **kwargs) -> Message:
        new = message
        insertion_list, separator = kwargs["insertion_list"], kwargs["separator"]
        old_text = message.text if message.text else message.caption
        new_text = copy(old_text)
        inserted_str = separator.join(insertion_list)
        new_text = new_text + "\n" + inserted_str
        if message.text is not None:
            if new_text != old_text:
                new = await message.edit_text(text=new_text)
        if message.caption is not None:
            if new_text != old_text:
                new = await message.edit_caption(caption=new_text)
        return new

