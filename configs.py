@AbirHasan2005
@Lookingforcommit
@synthimental
import json
from typing import Optional, Set, Dict
from copy import copy


class Config:
    HELP_TEXT: str = """
    This UserBot can forward messages from any chat to any other chat.
    
    👨🏻‍💻 **Commands:**
    
    • `!start` - Check if the userbot is alive.
    • `!help` - Get this help message.
    • `!stop` - Stop the userbot.
    
    • `!add_source`<ID> <name> - Add chat IDs to forward messages from.
    • `!add_target`<ID> <name> - Add chat IDs to forward messages to.
    
    • `!remove_source` - Remove chat IDs from the list of sources.
    • `!remove_target` - Remove chat IDs from the list of targets.
    
    • `!list` - List chat IDs of sources and targets.
    
    • `!link` - Connect a source channel to a destination channel.
    • `!unlink` - Disconnect a source channel from a destination channel.
    • `!list_links` - List all source to destination channel connections.
    """

    def __init__(self):
        try:
            with open("configs.json") as config_file:
                _data = json.loads(config_file.read())
            # Get This From my.telegram.org
            self.api_id: Optional[int] = _data.get("api_id")
            self.api_hash: Optional[str] = _data.get("api_hash")
            self.session_string: Optional[str] = _data.get("session_string")
            self.forward_from_chat_ids: Set[int] = set(_data.get("forward_from_chat_ids", []))
            self.forward_to_chat_ids: Set[int] = set(_data.get("forward_to_chat_ids", []))
            self.forward_as_copy: bool = _data.get("forward_as_copy", False)
            self.chat_id_to_name: Dict[int, str] = _data.get("chat_id_to_name", {})
            self.channel_links: Dict[int, Set[int]] = _data.get("channel_links", {})
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading configuration: {e}")
            raise

    def dump(self) -> None:
        # Convert sets to lists for JSON serialization
        data_dict = copy(vars(self))
        data_dict["forward_from_chat_ids"] = list(self.forward_from_chat_ids)
        data_dict["forward_to_chat_ids"] = list(self.forward_to_chat_ids)
        data_dict["channel_links"] = {k: list(v) for k, v in self.channel_links.items()}
        configs_json = json.dumps(data_dict, indent=2)
        with open("configs.json", "w") as f:
            f.write(configs_json)
