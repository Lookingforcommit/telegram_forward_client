# (c) @AbirHasan2005
# (c) @Lookingforcommit

import json
from typing import Optional, List


class Config:
    HELP_TEXT: str = """
        This UserBot can forward messages from any Chat to any other Chat.
        👨🏻‍💻 **Commands:**
        • `!start` - Check UserBot Alive or Not.
        • `!help` - Get this Message.
        • `!stop` - Stop forwarding & Restart Service.
        """

    def __init__(self):
        with open("configs.json") as config_file:
            _data = json.loads(config_file.read())
        # Get This From my.telegram.org
        self.api_id: Optional[int] = _data["api_id"]
        self.api_hash: Optional[str] = _data["api_hash"]
        self.session_string: Optional[str] = _data["session_string"]
        self.forward_from_chat_ids: List[int] = list(set(_data["forward_from_chat_ids"]))
        self.forward_to_chat_ids: List[int] = list(set(_data["forward_to_chat_ids"]))
        self.forward_filters: List[str] = list(set(_data["forward_filters"]))
        self.forward_as_copy: bool = _data["forward_as_copy"]
