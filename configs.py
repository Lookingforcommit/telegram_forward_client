import json
from typing import Optional, Set, Dict, List, Tuple, Any


def load_dict(data, dct_name: str) -> Dict[int, Any]:
    dct = data.get(dct_name, {})
    if dct:
        dct = {int(key): dct[key] for key in dct}
    return dct


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
    • `!add_scenario` - Start adding a new scenario.
    • `!end_scenario <name>` - Finish adding a scenario and save it.
    • `!remove_scenario <number>` - Remove a scenario.
    • `!list_scenarios` - List all scenarios.
    • `!add_stage <link_number> <scenario_number>` - Add a stage to a link.
    • `!remove_stage <stage_number>` - Remove a stage.
    • `!list_stages` - List all stages.
    """

    def __init__(self):
        self.load()
        self.scenario_input_mode: bool = False
        self.current_scenario: str = ""

    def dump(self) -> None:
        data_dict = {
            "api_id": self.api_id,
            "api_hash": self.api_hash,
            "session_string": self.session_string,
            "forward_from_chat_ids": list(self.forward_from_chat_ids),
            "forward_to_chat_ids": list(self.forward_to_chat_ids),
            "forward_as_copy": self.forward_as_copy,
            "links": self.links,
            "link_counter": self.link_counter,
            "scenarios": self.scenarios,
            "scenario_counter": self.scenario_counter,
            "stages": self.stages,
            "stage_counter": self.stage_counter
        }
        configs_json = json.dumps(data_dict, indent=2)
        with open("configs.json", "w") as f:
            f.write(configs_json)

    def load(self) -> None:
        with open("configs.json") as config_file:
            _data = json.loads(config_file.read())
        self.api_id: Optional[int] = _data["api_id"]
        self.api_hash: Optional[str] = _data["api_hash"]
        self.session_string: Optional[str] = _data["session_string"]
        self.forward_from_chat_ids: Set[int] = set(_data["forward_from_chat_ids"])
        self.forward_to_chat_ids: Set[int] = set(_data["forward_to_chat_ids"])
        self.forward_as_copy: bool = _data["forward_as_copy"]
        self.links: Dict[int, List[Tuple[int, int]]] = load_dict(_data, "links")
        self.link_counter: int = _data.get("link_counter", 0)
        self.scenarios: Dict[int, Tuple[str, str]] = load_dict(_data, "scenarios")
        self.scenario_counter: int = _data.get("scenario_counter", 0)
        self.stages: Dict[int, Tuple[int, int]] = load_dict(_data, "stages")  # {stage_number: (link_number, scenario_number)}
        self.stage_counter: int = _data.get("stage_counter", 0)

    def get_all_link_numbers(self) -> Set[int]:
        return set(number for links in self.links.values() for _, number in links)


# Создайте экземпляр класса Config
CONFIGS = Config()
