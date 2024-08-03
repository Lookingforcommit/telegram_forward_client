from pyrogram import Client
from pyrogram.types import Message


async def execute_scenarios(client: Client, message: Message, link_number: int) -> Message:
    from configs import CONFIGS  # Import here to avoid circular imports
    print(f"Executing scenarios for link number: {link_number}")
    modified_message = message
    for stage_number, (stage_link_number, scenario_number) in CONFIGS.stages.items():
        print(f"Checking stage {stage_number}: link {stage_link_number}, scenario {scenario_number}")
        if stage_link_number == link_number:
            print(f"Executing scenario {scenario_number}")
            scenario_name, scenario_code = CONFIGS.scenarios[scenario_number]
            try:
                # Create a new local scope for each scenario
                local_scope = {'client': client, 'message': modified_message}
                exec(scenario_code, globals(), local_scope)
                # Get the potentially modified message from the local scope
                modified_message = local_scope['message']
                print(f"Scenario {scenario_number} executed successfully")
            except Exception as e:
                print(f"Error executing scenario #{scenario_number} '{scenario_name}': {str(e)}")
                import traceback
                print(traceback.format_exc())
                # If an error occurs, we'll return the original message
                return message
    print(f"All scenarios executed. Message modified: {modified_message != message}")
    return modified_message
