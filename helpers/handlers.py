# (c) @Lookingforcommit

import helpers.general_commands as general_commands
import helpers.targets_management as targets_management
import helpers.links_management as links_management
from helpers import scenarios_execution

HANDLERS_DICT = {
    "!start": general_commands.on_start_command,
    "!stop": general_commands.on_stop_command,
    "!help": general_commands.on_help_command,
    "!list": targets_management.on_list_command,
    "!add_source": targets_management.on_add_source_command,
    "!add_target": targets_management.on_add_target_command,
    "!remove_source": targets_management.on_remove_source_command,
    "!remove_target": targets_management.on_remove_target_command,
    "!list_links": links_management.on_list_links_command,
    "!link": links_management.on_link_command,
    "!unlink": links_management.on_unlink_command,
    "!list_scenarios": scenarios_execution.on_list_scenarios_command,
    "!list_stages": scenarios_execution.on_list_stages_command,
    "!add_stage": scenarios_execution.on_add_stage_command,
    "!remove_stage": scenarios_execution.on_remove_stage_command,
    "!get_scenario_info": scenarios_execution.on_get_scenario_info_command,
    "!get_stage_arguments": scenarios_execution.on_get_stage_arguments_command,
    "!set_stage_arguments": scenarios_execution.on_set_stage_arguments_command,
    "!set_preprocess_chat": scenarios_execution.on_set_preprocess_chat_command,
}
