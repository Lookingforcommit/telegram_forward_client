# (c) @AbirHasan2005
# (c) @Lookingforcommit
# (c) @synthimental

import json
from typing import Optional, Dict, Any

from helpers.utilities import load_dict_with_int_keys


class ScenariosConfig:
    def __init__(self):
        self.stages_arguments: Optional[Dict[int, Dict[str, Any]]] = None
        self.load()

    def dump(self) -> None:
        data_dict = {
            "stages_arguments": self.stages_arguments,
        }
        configs_json = json.dumps(data_dict, indent=2, ensure_ascii=False)
        with open("scenarios/scenarios_configs.json", "w") as f:
            f.write(configs_json)

    def load(self) -> None:
        try:
            with open("scenarios/scenarios_configs.json") as config_file:
                data = json.load(config_file)
        except FileNotFoundError:
            data = {}
        self.stages_arguments = load_dict_with_int_keys(data, "stages_arguments")
