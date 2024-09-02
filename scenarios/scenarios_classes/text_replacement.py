# (c) @Lookingforcommit

from pyrogram import Client
from pyrogram.types import Message
from copy import copy
import re

from scenarios.scenarios_classes.base import BaseScenario


class TextReplacementScenario(BaseScenario):
    DESCRIPTION = "Scenario that replaces text using replacement dictionary."
    ARGUMENTS_CONVERSION_FUNCTIONS = {
        "replacement_dict": dict,
        "parse_regex": bool
    }
    ARGUMENTS_INFO = {
        "replacement_dict": "Dict of format {old_str1: new_str1, old_str2: new_str2, ...}\n"
                            "It is possible to use regular expressions in strings",
        "parse_regex": "Boolean value which marks if you are using regular expressions in strings"
    }

    async def apply(self, client: Client, message: Message, **kwargs) -> Message:
        new = message
        if message.text is not None or message.caption is not None:
            replacement_dict, parse_regex = kwargs["replacement_dict"], kwargs["parse_regex"]
            old_text = message.text if message.text else message.caption
            new_text = copy(old_text)
            for pattern_str in replacement_dict:
                if parse_regex:
                    new_text = re.sub(pattern_str, replacement_dict[pattern_str], new_text)
                else:
                    new_text = new_text.replace(pattern_str, replacement_dict[pattern_str])
            if message.text is not None:
                if new_text != old_text:
                    new = await message.edit_text(new_text)
            if message.caption is not None:
                if new_text != old_text:
                    new = await message.edit_caption(new_text)
        return new
