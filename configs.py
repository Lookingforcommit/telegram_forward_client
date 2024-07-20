# (c) @AbirHasan2005
# (c) @Lookingforcommit
# (c) @synthimental

import json
from typing import Optional, Set, Dict, List, Tuple

class Config:
    HELP_TEXT: str = """
    🤖 This UserBot can forward messages from specific chats to linked chats.
    👨🏻‍💻 **Commands:**
    • `!start` - Check if the userbot is alive.
    • `!help` - Get this help message.
    • `!stop` - Stop the userbot.
    • `!add_source` - Add chat IDs to forward messages from.
    • `!add_target` - Add chat IDs to forward messages to.
    • `!remove_source` - Remove chat IDs from the list of sources.
    • `!remove_target` - Remove chat IDs from the list of targets.
    • `!list` - List chat IDs of sources and targets.
    • `!link` - Connect a source channel to a destination channel.
    • `!unlink` - Disconnect a source channel from a destination channel.
    • `!list_links` - List all source to destination channel connections.
    """

    def __init__(self):
        with open("configs.json") as config_file:
            _data = json.loads(config_file.read())
        self.api_id: Optional[int] = _data["api_id"]
        self.api_hash: Optional[str] = _data["api_hash"]
        self.session_string: Optional[str] = _data["session_string"]
        self.forward_from_chat_ids: Set[int] = set(_data["forward_from_chat_ids"])
        self.forward_to_chat_ids: Set[int] = set(_data["forward_to_chat_ids"])
        self.forward_as_copy: bool = _data["forward_as_copy"]
        self.links: Dict[int, List[Tuple[int, int]]] = _data.get("links", {})
        self.link_counter: int = _data.get("link_counter", 0)

    def dump(self) -> None:
        data_dict = {
            "api_id": self.api_id,
            "api_hash": self.api_hash,
            "session_string": self.session_string,
            "forward_from_chat_ids": list(self.forward_from_chat_ids),
            "forward_to_chat_ids": list(self.forward_to_chat_ids),
            "forward_as_copy": self.forward_as_copy,
            "links": self.links,
            "link_counter": self.link_counter
        }
        configs_json = json.dumps(data_dict, indent=2)
        with open("configs.json", "w") as f:
            f.write(configs_json)
