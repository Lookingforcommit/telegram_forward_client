# (c) @AbirHasan2005
# (c) @Lookingforcommit
# (c) @synthimental

import json
from typing import Optional, Set, Dict, List, Tuple, Union

from helpers.utilities import load_dict_with_int_keys


class Config:
    """
    Links and stages format:\n
    links: {forward_from1: [(forward_to1, link_id1), (forward_to2, link_id2), ...], ...}\n
    stages: {stage_number1: (link_number1, scenario_name1), ...}
    """
    HELP_TEXT: str = """
    🤖 This UserBot can forward messages from specific chats to linked chats.
    👨🏻‍💻 **Commands:**
    - `!start` - Check if the userbot is alive.
    - `!help` - Get this help message.
    - `!stop` - Stop the userbot.
    - `!list` - List chat IDs of sources and targets.
    - `!add_source` [chat_id_1 chat_id_2 ...] - Add chat IDs to forward messages from.
    - `!add_target` [chat_id_1 chat_id_2 ...] - Add chat IDs to forward messages to.
    - `!remove_source` [chat_id_1 chat_id_2 ...] - Remove chat IDs from the list of sources.
    - `!remove_target` [chat_id_1 chat_id_2 ...] - Remove chat IDs from the list of targets.
    - `!list_links` - List all source to destination channel connections.
    - `!link` [source_chat_id] [target_chat_id] - Connect a source channel to a destination channel.
    - `!unlink` [link_number] - Disconnect a source channel from a destination channel.
    - `!list_scenarios` - List all scenarios.
    - `!list_stages` - List all stages.
    - `!add_stage` [link_number] [scenario_name] [arguments_dictionary] - Add a stage to a link.
    - `!remove_stage` [stage_number] - Remove a stage.
    - `!get_scenario_info` [scenario_name] - Get detailed scenario info.
    - `!get_stage_arguments` [stage_number] - Get stage arguments.
    - `!set_stage_arguments` [stage_number] [arguments_dictionary] - Set stage arguments.
    - `!set_preprocess_chat` [chat_id] - Set chat for preprocessing messages prior to scenarios execution.
    """

    def __init__(self):
        self.api_id: Optional[int] = None
        self.api_hash: Optional[str] = None
        self.session_string: Optional[str] = None
        self.preprocess_chat_id: Optional[Union[int, str]] = None
        self.forward_from_chat_ids: Optional[Set[int]] = None
        self.forward_to_chat_ids: Optional[Set[int]] = None
        self.links: Optional[Dict[int, List[Tuple[int, int]]]] = None
        self.link_counter: Optional[int] = None
        self.stages: Optional[Dict[int, Tuple[int, str]]] = None
        self.stage_counter: Optional[int] = None
        self.load()
        self.is_running: bool = False

    def dump(self) -> None:
        data_dict = {
            "api_id": self.api_id,
            "api_hash": self.api_hash,
            "session_string": self.session_string,
            "preprocess_chat_id": self.preprocess_chat_id,
            "forward_from_chat_ids": list(self.forward_from_chat_ids),
            "forward_to_chat_ids": list(self.forward_to_chat_ids),
            "links": self.links,
            "link_counter": self.link_counter,
            "stages": self.stages,
            "stage_counter": self.stage_counter,
        }
        configs_json = json.dumps(data_dict, indent=2)
        with open("configs.json", "w") as f:
            f.write(configs_json)

    def load(self) -> None:
        with open("configs.json") as config_file:
            data = json.loads(config_file.read())
        self.api_id = data["api_id"]
        self.api_hash = data["api_hash"]
        self.session_string = data["session_string"]
        self.preprocess_chat_id = data.get("preprocess_chat_id", "me")
        self.forward_from_chat_ids = set(data["forward_from_chat_ids"])
        self.forward_to_chat_ids = set(data["forward_to_chat_ids"])
        self.links = load_dict_with_int_keys(data, "links")
        self.link_counter = data.get("link_counter", 0)
        self.stages = load_dict_with_int_keys(data, "stages")
        self.stage_counter = data.get("stage_counter", 0)

    def get_all_link_numbers(self) -> Set[int]:
        return set(number for links in self.links.values() for _, number in links)
