# (c) @Lookingforcommit

from pyrogram import Client
from pyrogram.types import Message, MessageEntity
from pyrogram.enums import MessageEntityType
from copy import deepcopy
from typing import List
import re

from scenarios.scenarios_classes.base import BaseScenario


class TextLinksDeletionScenario(BaseScenario):
    DESCRIPTION = "Scenario that deletes formatted hyperlinks using deletion list."
    ARGUMENTS_CONVERSION_FUNCTIONS = {
        "deletion_list": list,
        "parse_regex": bool
    }
    ARGUMENTS_INFO = {
        "deletion_list": "List of format [old_url1, old_url2, ...]\n"
                         "It is possible to use regular expressions in urls",
        "parse_regex": "Boolean value which marks if you are using regular expressions in urls"
    }

    @staticmethod
    def delete_entities_url(entities: List[MessageEntity], deletion_list: List[str],
                            parse_regex: bool) -> List[MessageEntity]:
        ans_list = []
        for i in range(len(entities)):
            entity = entities[i]
            if entity.type == MessageEntityType.TEXT_LINK:
                trig = True
                for url_pattern in deletion_list:
                    if parse_regex:
                        if re.fullmatch(url_pattern, entity.url):
                            trig = False
                            break
                    else:
                        if entity.url in deletion_list:
                            trig = False
                            break
                if trig:
                    ans_list.append(entity)
        return ans_list

    async def apply(self, client: Client, message: Message, **kwargs) -> Message:
        new = message
        if message.text is not None or message.caption is not None:
            deletion_list, parse_regex = kwargs["deletion_list"], kwargs["parse_regex"]
            old_text = message.text if message.text else message.caption
            old_entities = message.entities if message.entities else message.caption_entities
            new_entities = deepcopy(old_entities)
            if new_entities is not None:
                new_entities = self.delete_entities_url(new_entities, deletion_list, parse_regex)
            if message.text is not None:
                if new_entities != old_entities:
                    new = await message.edit_text(text=old_text, entities=new_entities)
            if message.caption is not None:
                if new_entities != old_entities:
                    new = await message.edit_caption(caption=old_text, caption_entities=new_entities)
        return new

