# (c) @Lookingforcommit

from pyrogram import Client
from pyrogram.types import Message
from copy import copy
import re

from scenarios.scenarios_classes.base import BaseScenario


class TextDeletionScenario(BaseScenario):
    DESCRIPTION = "Scenario that deletes text using deletion list."
    ARGUMENTS_CONVERSION_FUNCTIONS = {
        "deletion_list": list,
        "parse_regex": bool
    }
    ARGUMENTS_INFO = {
        "deletion_list": "List of format [old_str1, old_str2, ...]\n"
                         "It is possible to use regular expressions in strings",
        "parse_regex": "Boolean value which marks if you are using regular expressions in strings"
    }

    async def apply(self, client: Client, message: Message, **kwargs) -> Message:
        new = message
        if message.text is not None or message.caption is not None:
            deletion_list, parse_regex = kwargs["deletion_list"], kwargs["parse_regex"]
            old_text = message.text if message.text else message.caption
            new_text = copy(old_text)
            for pattern_str in deletion_list:
                if parse_regex:
                    new_text = re.sub(pattern_str, "", new_text)
                else:
                    new_text = new_text.replace(pattern_str, "")
            if message.text is not None:
                if new_text != old_text:
                    new = await message.edit_text(text=new_text)
            if message.caption is not None:
                if new_text != old_text:
                    new = await message.edit_caption(caption=new_text)
        return new

