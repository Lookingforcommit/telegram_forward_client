# (c) @AbirHasan2005
# (c) @Lookingforcommit

import json
from typing import Optional, Set
from copy import copy


class Config:
    HELP_TEXT: str = """
    This UserBot can forward messages from any Chat to any other Chat.
    👨🏻‍💻 **Commands:**
    • `!start` - Check if userbot is alive.
    • `!help` - Get this message.
    • `!stop` - Stop forwarding.
    • `!add_forward_to_chat` - Add chat_ids to forward messages to. Separate with space.
    • `!add_forward_from_chat` - Add chat_ids to forward messages from. Separate with space.
    • `!remove_forward_to_chat` - Remove chat_ids to forward messages to. Separate with space.
    • `!remove_forward_from_chat` - Remove chat_ids to forward messages from. Separate with space.
    • `!list_forward_to_chat` - List chat_ids of the chats you are forwarding messages to. Separate with space.
    • `!list_forward_from_chat` - List chat_ids of the chats you are forwarding messages from. Separate with space.
    """

    def __init__(self):
        with open("configs.json") as config_file:
            _data = json.loads(config_file.read())
        # Get This From my.telegram.org
        self.api_id: Optional[int] = _data["api_id"]
        self.api_hash: Optional[str] = _data["api_hash"]
        self.session_string: Optional[str] = _data["session_string"]
        self.forward_from_chat_ids: Set[int] = set(_data["forward_from_chat_ids"])
        self.forward_to_chat_ids: Set[int] = set(_data["forward_to_chat_ids"])
        self.forward_as_copy: bool = _data["forward_as_copy"]

    def dump(self) -> None:
        data_dict = copy(vars(self))
        data_dict["forward_from_chat_ids"] = list(self.forward_from_chat_ids)
        data_dict["forward_to_chat_ids"] = list(self.forward_to_chat_ids)
        configs_json = json.dumps(data_dict, indent=2)
        with open("configs.json", "w") as f:
            f.write(configs_json)
