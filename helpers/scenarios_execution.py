# (c) @Lookingforcommit
# (c) @synthimental

from pyrogram import Client
from pyrogram.types import Message
import json

from configs import Config
from scenarios.scenarios_classes.base import BaseScenario
from scenarios.scenarios_configs import ScenariosConfig
from scenarios.scenarios_mapping import OBJECTS_MAPPING
from helpers.forwarder import forward_message
from exceptions import ScenarioException, PreprocessCopyingException


async def on_list_scenarios_command(message: Message, **kwargs) -> Message:
    if len(OBJECTS_MAPPING) == 0:
        return await message.reply_text("🤖 No scenarios available.")
    scenarios_list = ["🤖 List of scenarios:"]
    for name in OBJECTS_MAPPING:
        scenario_object = OBJECTS_MAPPING[name]
        scenarios_list.append(f"Scenario `{name}`:\n{scenario_object.DESCRIPTION}")
    await message.reply_text("\n\n".join(scenarios_list))


async def on_list_stages_command(message: Message, configs: Config, **kwargs) -> Message:
    if not configs.stages:
        return await message.reply_text("🤖 No stages available.")
    stages_list = ["🤖 List of stages:"]
    for stage_number, (link_number, scenario_name) in configs.stages.items():
        stages_list.append(
            f"#{stage_number} Stage:\nScenario `{scenario_name}` -> #{link_number} Link")
    await message.reply_text("\n\n".join(stages_list))


def update_scenarios_configs(new_configs: str, scenarios_configs: ScenariosConfig, scenario_object: BaseScenario,
                             stage_number: int) -> None:
    new_configs = json.loads(new_configs)
    processed_arguments = scenario_object.process_arguments(new_configs)
    scenarios_configs.stages_arguments[stage_number] = processed_arguments
    scenarios_configs.dump()


async def on_add_stage_command(message: Message, configs: Config, scenarios_configs: ScenariosConfig,
                               **kwargs) -> Message:
    parts = message.text.split(maxsplit=3)
    if len(parts) != 4:
        return await message.reply_text("🤖 Usage: !add_stage [link_number] [scenario_name] [arguments_json]")
    try:
        link_number = int(parts[1])
        scenario_name = parts[2]
        scenario_object = OBJECTS_MAPPING[scenario_name]
    except ValueError:
        return await message.reply_text("🤖 Invalid link number.")
    except KeyError:
        return await message.reply_text("🤖 Invalid scenario name.")
    if link_number not in configs.get_all_link_numbers():
        return await message.reply_text("🤖 Link not found.")
    if scenario_name not in OBJECTS_MAPPING:
        return await message.reply_text("🤖 Scenario not found.")
    stage_number = configs.stage_counter + 1
    try:
        update_scenarios_configs(parts[3], scenarios_configs, scenario_object, stage_number)
        configs.stages[stage_number] = (link_number, scenario_name)
        configs.stage_counter = stage_number
        configs.dump()
        await message.reply_text(f"🤖 Stage #{stage_number} added successfully.")
    except Exception as e:
        await message.reply_text(f"🤖 Incorrect arguments for stage #{stage_number}."
                                 f" \nError: {e}")


async def on_remove_stage_command(message: Message, configs: Config, scenarios_configs: ScenariosConfig,
                                  **kwargs) -> Message:
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !remove_stage [stage_number]")
    try:
        stage_number = int(parts[1])
    except ValueError:
        return await message.reply_text("🤖 Invalid stage number.")
    if stage_number not in configs.stages:
        return await message.reply_text("🤖 Stage not found.")
    del configs.stages[stage_number]
    del scenarios_configs.stages_arguments[stage_number]
    configs.dump()
    scenarios_configs.dump()
    await message.reply_text(f"🤖 Stage #{stage_number} removed successfully.")


async def on_get_scenario_info_command(message: Message, **kwargs) -> Message:
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !get_scenario_info [scenario_name]")
    scenario_name = parts[1]
    if scenario_name not in OBJECTS_MAPPING:
        return await message.reply_text("🤖 Invalid scenario name.")
    scenario_object = OBJECTS_MAPPING[scenario_name]
    description = scenario_object.DESCRIPTION
    arguments_info = scenario_object.ARGUMENTS_INFO
    arguments_info = "\n".join([f"`{key}`: {arguments_info[key]}" for key in arguments_info])
    await message.reply_text(f"🤖 Scenario `{scenario_name}`:\n{description}\n"
                             f"Arguments: \n{arguments_info}")


async def on_get_stage_arguments_command(message: Message, configs: Config, scenarios_configs: ScenariosConfig,
                                         **kwargs) -> Message:
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !get_stage_arguments [stage_number]")
    try:
        stage_number = int(parts[1])
    except ValueError:
        return await message.reply_text("🤖 Invalid stage number.")
    if stage_number not in configs.stages:
        return await message.reply_text("🤖 Stage not found.")
    stage_arguments = scenarios_configs.stages_arguments[stage_number]
    await message.reply_text(f"🤖 Stage `{stage_number}` arguments:\n{stage_arguments}")


async def on_set_stage_arguments_command(message: Message, configs: Config,
                                         scenarios_configs: ScenariosConfig, **kwargs) -> Message:
    parts = message.text.split(maxsplit=2)
    if len(parts) != 3:
        return await message.reply_text("🤖 Usage: !set_stage_arguments [stage_number] [arguments_json]")
    try:
        stage_number = int(parts[1])
    except ValueError:
        return await message.reply_text("🤖 Invalid stage number.")
    if stage_number not in configs.stages:
        return await message.reply_text("🤖 Stage not found.")
    scenario_name = configs.stages[stage_number][1]
    scenario_object = OBJECTS_MAPPING[scenario_name]
    try:
        update_scenarios_configs(parts[2], scenarios_configs, scenario_object, stage_number)
        await message.reply_text(f"🤖 Arguments for stage #{stage_number} set successfully")
    except Exception as e:
        await message.reply_text(f"🤖 Incorrect arguments for stage #{stage_number}."
                                 f" \nError: {e}")


async def on_set_preprocess_chat_command(message: Message, configs: Config, **kwargs) -> Message:
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !set_preprocess_chat [chat_id]")
    try:
        chat_id = int(parts[1])
    except ValueError:
        return await message.reply_text("🤖 Invalid chat id.")
    configs.preprocess_chat_id = chat_id
    configs.dump()
    await message.reply_text(f"🤖 Chat `{chat_id}` has been set for scenarios preprocessing.")


async def execute_scenarios(client: Client, message: Message, link_number: int, configs: Config,
                            scenarios_configs: ScenariosConfig) -> Message:
    links_and_scenarios = list(filter(lambda item: item[1][0] == link_number, configs.stages.items()))
    if len(links_and_scenarios) == 0:
        return message
    try:
        edited_message = await forward_message(client, message, {configs.preprocess_chat_id})
    except Exception as e:
        raise PreprocessCopyingException(message.id, str(e))
    for stage_number, (stage_link_number, scenario_name) in links_and_scenarios:
        scenario_object = OBJECTS_MAPPING[scenario_name]
        scenario_arguments = scenarios_configs.stages_arguments[stage_number]
        try:
            edited_message = await scenario_object.apply(client, edited_message, **scenario_arguments)
        except Exception as e:
            raise ScenarioException(stage_number, scenario_name, str(e))
    return edited_message
