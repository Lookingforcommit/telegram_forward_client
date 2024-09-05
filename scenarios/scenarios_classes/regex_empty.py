from pyrogram import Client
from pyrogram.types import Message
import re

from scenarios.scenarios_classes.base import BaseScenario

class RegexEmptyScenario(BaseScenario):
    DESCRIPTION = "Scenario that empties the message if it matches a regex pattern, unless it contains a specific link."
    ARGUMENTS_CONVERSION_FUNCTIONS = {
        "regex_pattern": str,
        "exception_link": str
    }
    ARGUMENTS_INFO = {
        "regex_pattern": "Regular expression pattern to match against the message text",
        "exception_link": "If this link is present in the message, it will not be emptied"
    }

    async def apply(self, client: Client, message: Message, **kwargs) -> Message:
        regex_pattern = kwargs["regex_pattern"]
        exception_link = kwargs["exception_link"]
        if message.text is not None or message.caption is not None:
            text = message.text if message.text else message.caption
            if exception_link in text:
                return message
            if re.fullmatch(regex_pattern, text):
                message = None
        return message
