from pyrogram import Client
from pyrogram.types import Message

from configs import Config


async def on_add_scenario_command(client: Client, message: Message, configs: Config) -> None:
    print("Entering scenario input mode")
    configs.scenario_input_mode = True
    configs.current_scenario = ""
    print(f"Scenario input mode: {configs.scenario_input_mode}")
    await message.reply_text("🤖 Enter your scenario code. Use !end_scenario <name> when finished.")


async def on_end_scenario_command(client: Client, message: Message, configs: Config) -> Message:
    if not configs.scenario_input_mode:
        return await message.reply_text("🤖 No scenario input in progress.")
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !end_scenario <name>")
    name = parts[1]
    # Encoding check
    try:
        configs.current_scenario.encode('utf-8')
    except UnicodeEncodeError:
        return await message.reply_text(
            "🤖 Error: Scenario contains invalid characters. Please use only UTF-8 compatible characters.")
    scenario_number = configs.scenario_counter + 1
    configs.save_scenario(name, configs.current_scenario)
    configs.scenarios[scenario_number] = (name, configs.current_scenario)
    configs.scenario_counter = scenario_number
    configs.scenario_input_mode = False
    configs.current_scenario = ""
    configs.dump()
    await message.reply_text(f"🤖 Scenario #{scenario_number} '{name}' added successfully.")


async def on_remove_scenario_command(client: Client, message: Message, configs: Config) -> Message:
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !remove_scenario <number>")
    try:
        scenario_number = int(parts[1])
    except ValueError:
        return await message.reply_text("🤖 Invalid scenario number.")
    if scenario_number not in configs.scenarios:
        return await message.reply_text("🤖 Scenario not found.")
    name, _ = configs.scenarios[scenario_number]
    configs.remove_scenario_file(name)
    del configs.scenarios[scenario_number]
    configs.dump()
    await message.reply_text(f"🤖 Scenario #{scenario_number} removed successfully.")


async def on_list_scenarios_command(client: Client, message: Message, configs: Config) -> Message:
    if not configs.scenarios:
        return await message.reply_text("🤖 No scenarios available.")
    scenarios_list = ["🤖 List of scenarios:"]
    for number, (name, code) in configs.scenarios.items():
        scenarios_list.append(f"#{number} Scenario {name}:\n```\n{code}\n```")
    await message.reply_text("\n\n".join(scenarios_list))


async def on_add_stage_command(client: Client, message: Message, configs: Config) -> Message:
    parts = message.text.split()
    if len(parts) != 3:
        return await message.reply_text("🤖 Usage: !add_stage <link_number> <scenario_number>")
    try:
        link_number = int(parts[1])
        scenario_number = int(parts[2])
    except ValueError:
        return await message.reply_text("🤖 Invalid link or scenario number.")
    if link_number not in configs.get_all_link_numbers():
        return await message.reply_text("🤖 Link not found.")
    if scenario_number not in configs.scenarios:
        return await message.reply_text("🤖 Scenario not found.")
    stage_number = configs.stage_counter + 1
    configs.stages[stage_number] = (link_number, scenario_number)
    configs.stage_counter = stage_number
    configs.dump()
    await message.reply_text(f"🤖 Stage #{stage_number} added successfully.")


async def on_remove_stage_command(client: Client, message: Message, configs: Config) -> Message:
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !remove_stage <stage_number>")
    try:
        stage_number = int(parts[1])
    except ValueError:
        return await message.reply_text("🤖 Invalid stage number.")
    if stage_number not in configs.stages:
        return await message.reply_text("🤖 Stage not found.")
    del configs.stages[stage_number]
    configs.dump()
    await message.reply_text(f"🤖 Stage #{stage_number} removed successfully.")


async def on_list_stages_command(client: Client, message: Message, configs: Config) -> Message:
    if not configs.stages:
        return await message.reply_text("🤖 No stages available.")
    stages_list = ["🤖 List of stages:"]
    for stage_number, (link_number, scenario_number) in configs.stages.items():
        scenario_name = configs.scenarios.get(scenario_number, ("Unknown", ""))[0]
        stages_list.append(
            f"#{stage_number} Stage:\n#{scenario_number} Scenario '{scenario_name}' -> #{link_number} Link")
    await message.reply_text("\n\n".join(stages_list))
    # Add this part to print debug information
    print("Current stages configuration:")
    print(configs.stages)
    print("Current scenarios configuration:")
    print(configs.scenarios)
    print("Current links configuration:")
    print(configs.links)


async def execute_scenarios(client: Client, message: Message, link_number: int, configs: Config) -> Message:
    print(f"Executing scenarios for link number: {link_number}")
    modified_message = message
    for stage_number, (stage_link_number, scenario_number) in configs.stages.items():
        print(f"Checking stage {stage_number}: link {stage_link_number}, scenario {scenario_number}")
        if stage_link_number == link_number:
            print(f"Executing scenario {scenario_number}")
            scenario_name, scenario_code = configs.scenarios[scenario_number]
            try:
                scenario_code = scenario_code.encode('utf-8').decode('utf-8')
                # Create a new local scope for each scenario
                local_scope = {'client': client, 'message': modified_message}
                exec(scenario_code, globals(), local_scope)
                # Get the potentially modified message from the local scope
                new_message = local_scope['message']
                if new_message != modified_message:
                    modified_message = new_message
                    print(f"Scenario {scenario_number} modified the message")
                else:
                    print(f"Scenario {scenario_number} did not modify the message")
            except UnicodeEncodeError:
                print(f"Error: Scenario {scenario_number} contains invalid characters")
            except Exception as e:
                print(f"Error executing scenario #{scenario_number} '{scenario_name}': {str(e)}")
                import traceback
                print(traceback.format_exc())
    print(f"All scenarios executed. Message modified: {modified_message != message}")
    return modified_message
