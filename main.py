# (c) @AbirHasan2005
# (c) @Lookingforcommit
# (c) @synthimental

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums.chat_type import ChatType
from pyrogram.errors import FloodWait
import pyrogram.utils as utils

from configs import CONFIGS
from helpers.forwarder import forward_message


def get_peer_type(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"


utils.get_peer_type = get_peer_type
RUN = {"is_running": True}
user = Client(
    name='pyrogram',
    api_hash=CONFIGS.api_hash,
    api_id=CONFIGS.api_id,
    in_memory=True,
    session_string=CONFIGS.session_string
)


async def on_start_command(client: Client, message: Message):
    if not RUN["is_running"]:
        RUN["is_running"] = True
    await message.edit(
        text=f"🤖 Hi, **{(await client.get_me()).first_name}**!\nThis is a forwarder userbot by @Lookingforcommit",
        disable_web_page_preview=True)


async def on_stop_command(message: Message):
    if RUN["is_running"]:
        RUN["is_running"] = False
    return await message.edit("🤖 Userbot stopped!\n\nSend `!start` to start userbot again.")


async def on_help_command(message: Message):
    await message.edit(text=CONFIGS.HELP_TEXT, disable_web_page_preview=True)


async def get_chat_name(client: Client, chat_id: int) -> str:
    try:
        chat = await client.get_chat(chat_id)
        return chat.title or chat.first_name or str(chat_id)
    except Exception:
        return str(chat_id)


async def on_add_command(client: Client, message: Message, is_source: bool):
    if len(message.text.split(" ", 1)) < 2:
        return await message.reply_text("🤖 No chat_id specified")

    chat_ids = message.text.split(" ")[1:]
    added_chats = []

    for chat_id in chat_ids:
        try:
            chat_id = int(chat_id)
            chat_name = await get_chat_name(client, chat_id)
            if is_source:
                if chat_id not in CONFIGS.forward_from_chat_ids:
                    CONFIGS.forward_from_chat_ids.add(chat_id)
                    added_chats.append(f"{chat_name}")
            else:
                if chat_id not in CONFIGS.forward_to_chat_ids:
                    CONFIGS.forward_to_chat_ids.add(chat_id)
                    added_chats.append(f"{chat_name}")
        except ValueError:
            await message.reply_text(f"🤖 Invalid chat_id: {chat_id}")

    if added_chats:
        CONFIGS.dump()
        response = "🤖 Added successfully:\n" + "\n".join([f"{name} added successfully!" for name in added_chats])
        await message.reply_text(response)
    else:
        await message.reply_text("🤖 No new chats were added.")


async def on_remove_command(client: Client, message: Message, is_source: bool):
    if len(message.text.split(" ", 1)) < 2:
        return await message.reply_text("🤖 No chat_id specified")

    chat_ids = message.text.split(" ")[1:]
    removed_chats = []

    for chat_id in chat_ids:
        try:
            chat_id = int(chat_id)
            chat_name = await get_chat_name(client, chat_id)
            if is_source:
                if chat_id in CONFIGS.forward_from_chat_ids:
                    CONFIGS.forward_from_chat_ids.remove(chat_id)
                    removed_chats.append(f"{chat_name}")
            else:
                if chat_id in CONFIGS.forward_to_chat_ids:
                    CONFIGS.forward_to_chat_ids.remove(chat_id)
                    removed_chats.append(f"{chat_name}")
        except ValueError:
            await message.reply_text(f"🤖 Invalid chat_id: {chat_id}")

    if removed_chats:
        CONFIGS.dump()
        response = "🤖 Removed successfully:\n" + "\n".join([f"{name} removed successfully!" for name in removed_chats])
        await message.reply_text(response)
    else:
        await message.reply_text("🤖 No chats were removed.")


async def on_list_command(client: Client, message: Message):
    if not CONFIGS.forward_from_chat_ids and not CONFIGS.forward_to_chat_ids:
        return await message.reply_text("🤖 No chats have been added yet.")

    response = []
    if CONFIGS.forward_from_chat_ids:
        source_list = ["🤖 Source:"]
        for chat_id in CONFIGS.forward_from_chat_ids:
            chat_name = await get_chat_name(client, chat_id)
            source_list.append(f"{chat_name}(`{chat_id}`)")
        response.extend(source_list)

    if CONFIGS.forward_to_chat_ids:
        if response:
            response.append("")
        target_list = ["🤖 Target:"]
        for chat_id in CONFIGS.forward_to_chat_ids:
            chat_name = await get_chat_name(client, chat_id)
            target_list.append(f"{chat_name}(`{chat_id}`)")
        response.extend(target_list)

    await message.reply_text("\n".join(response))


async def on_link_command(client: Client, message: Message):
    parts = message.text.split()
    if len(parts) != 3:
        return await message.reply_text("🤖 Usage: !link <source_id> <target_id>")
    try:
        source_id, target_id = map(int, parts[1:3])
    except ValueError:
        return await message.reply_text("🤖 Invalid chat IDs. Please use numeric IDs.")
    if source_id not in CONFIGS.forward_from_chat_ids:
        return await message.reply_text("🤖 Source ID is not in the list of source chats.")
    if target_id not in CONFIGS.forward_to_chat_ids:
        return await message.reply_text("🤖 Target ID is not in the list of target chats.")
    used_numbers = set()
    for links in CONFIGS.links.values():
        used_numbers.update(number for _, number in links)
    link_number = 1
    while link_number in used_numbers:
        link_number += 1
    if source_id not in CONFIGS.links:
        CONFIGS.links[source_id] = []
    CONFIGS.links[source_id].append((target_id, link_number))
    CONFIGS.link_counter = max(CONFIGS.link_counter, link_number)
    print(CONFIGS.links)
    CONFIGS.dump()
    source_name = await get_chat_name(client, source_id)
    target_name = await get_chat_name(client, target_id)
    await message.reply_text(
        f"🤖 Linked: {source_name}(`{source_id}`) -> {target_name}(`{target_id}`) - Link #{link_number}")


async def on_unlink_command(client: Client, message: Message):
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !unlink <link_number>")

    try:
        link_number = int(parts[1])
    except ValueError:
        return await message.reply_text("🤖 Invalid link number. Please use a numeric value.")
    found = False
    for source_id, links in CONFIGS.links.items():
        for i, (target_id, number) in enumerate(links):
            if number == link_number:
                del CONFIGS.links[source_id][i]
                if not CONFIGS.links[source_id]:
                    del CONFIGS.links[source_id]
                CONFIGS.link_counter -= 1
                for s_id in CONFIGS.links:
                    CONFIGS.links[s_id] = [(t_id, n if n < link_number else n - 1) for t_id, n in CONFIGS.links[s_id]]
                CONFIGS.dump()
                source_name = await get_chat_name(client, source_id)
                target_name = await get_chat_name(client, target_id)
                await message.reply_text(
                    f"🤖 Unlinked: {source_name}(`{source_id}`) -> {target_name}(`{target_id}`) - Link #{link_number}")
                found = True
                break
        if found:
            break
    if not found:
        await message.reply_text("🤖 This link number does not exist.")


async def on_list_links_command(client: Client, message: Message):
    if not CONFIGS.links:
        return await message.reply_text("🤖 No active links.")

    links_list = ["🤖 List of links:"]
    for source_id, links in CONFIGS.links.items():
        source_name = await get_chat_name(client, source_id)
        for target_id, link_number in links:
            target_name = await get_chat_name(client, target_id)
            links_list.append(f"#{link_number} Link:\n{source_name}(`{source_id}`) -> {target_name}(`{target_id}`)")

    await message.reply_text("\n\n".join(links_list))


async def on_add_scenario_command(client: Client, message: Message):
    print("Entering scenario input mode")
    CONFIGS.scenario_input_mode = True
    CONFIGS.current_scenario = ""
    print(f"Scenario input mode: {CONFIGS.scenario_input_mode}")
    await message.reply_text("🤖 Enter your scenario code. Use !end_scenario <name> when finished.")


async def on_end_scenario_command(client: Client, message: Message):
    if not CONFIGS.scenario_input_mode:
        return await message.reply_text("🤖 No scenario input in progress.")
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !end_scenario <name>")
    name = parts[1]

    # Добавляем проверку кодировки
    try:
        CONFIGS.current_scenario.encode('utf-8')
    except UnicodeEncodeError:
        return await message.reply_text(
            "🤖 Error: Scenario contains invalid characters. Please use only UTF-8 compatible characters.")

    scenario_number = CONFIGS.scenario_counter + 1
    CONFIGS.save_scenario(name, CONFIGS.current_scenario)
    CONFIGS.scenarios[scenario_number] = (name, CONFIGS.current_scenario)
    CONFIGS.scenario_counter = scenario_number
    CONFIGS.scenario_input_mode = False
    CONFIGS.current_scenario = ""
    CONFIGS.dump()
    await message.reply_text(f"🤖 Scenario #{scenario_number} '{name}' added successfully.")


async def on_remove_scenario_command(client: Client, message: Message):
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !remove_scenario <number>")
    try:
        scenario_number = int(parts[1])
    except ValueError:
        return await message.reply_text("🤖 Invalid scenario number.")
    if scenario_number not in CONFIGS.scenarios:
        return await message.reply_text("🤖 Scenario not found.")
    name, _ = CONFIGS.scenarios[scenario_number]
    CONFIGS.remove_scenario_file(name)
    del CONFIGS.scenarios[scenario_number]
    CONFIGS.dump()
    await message.reply_text(f"🤖 Scenario #{scenario_number} removed successfully.")


async def on_list_scenarios_command(client: Client, message: Message):
    if not CONFIGS.scenarios:
        return await message.reply_text("🤖 No scenarios available.")

    scenarios_list = ["🤖 List of scenarios:"]
    for number, (name, code) in CONFIGS.scenarios.items():
        scenarios_list.append(f"#{number} Scenario {name}:\n```\n{code}\n```")

    await message.reply_text("\n\n".join(scenarios_list))


async def on_add_stage_command(client: Client, message: Message):
    parts = message.text.split()
    if len(parts) != 3:
        return await message.reply_text("🤖 Usage: !add_stage <link_number> <scenario_number>")
    try:
        link_number = int(parts[1])
        scenario_number = int(parts[2])
    except ValueError:
        return await message.reply_text("🤖 Invalid link or scenario number.")
    if link_number not in CONFIGS.get_all_link_numbers():
        return await message.reply_text("🤖 Link not found.")
    if scenario_number not in CONFIGS.scenarios:
        return await message.reply_text("🤖 Scenario not found.")
    stage_number = CONFIGS.stage_counter + 1
    CONFIGS.stages[stage_number] = (link_number, scenario_number)
    CONFIGS.stage_counter = stage_number
    CONFIGS.dump()
    await message.reply_text(f"🤖 Stage #{stage_number} added successfully.")


async def on_remove_stage_command(client: Client, message: Message):
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !remove_stage <stage_number>")
    try:
        stage_number = int(parts[1])
    except ValueError:
        return await message.reply_text("🤖 Invalid stage number.")
    if stage_number not in CONFIGS.stages:
        return await message.reply_text("🤖 Stage not found.")
    del CONFIGS.stages[stage_number]
    CONFIGS.dump()
    await message.reply_text(f"🤖 Stage #{stage_number} removed successfully.")


async def on_list_stages_command(client: Client, message: Message):
    if not CONFIGS.stages:
        return await message.reply_text("🤖 No stages available.")

    stages_list = ["🤖 List of stages:"]
    for stage_number, (link_number, scenario_number) in CONFIGS.stages.items():
        scenario_name = CONFIGS.scenarios.get(scenario_number, ("Unknown", ""))[0]
        stages_list.append(
            f"#{stage_number} Stage:\n#{scenario_number} Scenario '{scenario_name}' -> #{link_number} Link")

    await message.reply_text("\n\n".join(stages_list))

    # Add this part to print debug information
    print("Current stages configuration:")
    print(CONFIGS.stages)
    print("Current scenarios configuration:")
    print(CONFIGS.scenarios)
    print("Current links configuration:")
    print(CONFIGS.links)


async def execute_scenarios(client: Client, message: Message, link_number: int) -> Message:
    print(f"Executing scenarios for link number: {link_number}")
    modified_message = message
    for stage_number, (stage_link_number, scenario_number) in CONFIGS.stages.items():
        print(f"Checking stage {stage_number}: link {stage_link_number}, scenario {scenario_number}")
        if stage_link_number == link_number:
            print(f"Executing scenario {scenario_number}")
            scenario_name, scenario_code = CONFIGS.scenarios[scenario_number]
            try:
                # Попытка декодировать сценарий в UTF-8
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


@user.on_raw_update(group=1)
async def get_session_string(client: Client, message: Message, users, chats):
    if CONFIGS.session_string == "":
        CONFIGS.session_string = await client.export_session_string()
        CONFIGS.dump()


@user.on_message(filters.all, group=0)
async def main(client: Client, message: Message):
    bot_command = (message.chat is not None and message.chat.type == ChatType.PRIVATE and message.from_user.is_self
                   and message.text is not None)
    if bot_command:
        if message.text == "!start":
            await on_start_command(client, message)
        elif message.text == "!stop":
            await on_stop_command(message)
        elif message.text == "!help":
            await on_help_command(message)
        elif message.text.startswith("!add_source"):
            await on_add_command(client, message, is_source=True)
        elif message.text.startswith("!add_target"):
            await on_add_command(client, message, is_source=False)
        elif message.text.startswith("!remove_source"):
            await on_remove_command(client, message, is_source=True)
        elif message.text.startswith("!remove_target"):
            await on_remove_command(client, message, is_source=False)
        elif message.text == "!list":
            await on_list_command(client, message)
        elif message.text.startswith("!link"):
            await on_link_command(client, message)
        elif message.text.startswith("!unlink"):
            await on_unlink_command(client, message)
        elif message.text == "!list_links":
            await on_list_links_command(client, message)
        elif message.text == "!add_scenario":
            await on_add_scenario_command(client, message)
        elif message.text.startswith("!end_scenario"):
            await on_end_scenario_command(client, message)
        elif message.text.startswith("!remove_scenario"):
            await on_remove_scenario_command(client, message)
        elif message.text == "!list_scenarios":
            await on_list_scenarios_command(client, message)
        elif message.text.startswith("!add_stage"):
            await on_add_stage_command(client, message)
        elif message.text.startswith("!remove_stage"):
            await on_remove_stage_command(client, message)
        elif message.text == "!list_stages":
            await on_list_stages_command(client, message)
        elif CONFIGS.scenario_input_mode and message.from_user.is_self:
            CONFIGS.current_scenario += message.text + "\n"
    elif message.chat is not None and message.chat.id in CONFIGS.forward_from_chat_ids and RUN["is_running"]:
        if message.chat.id in CONFIGS.links:
            for target_id, link_number in CONFIGS.links[message.chat.id]:
                try:
                    # Apply scenarios before forwarding
                    modified_message = await execute_scenarios(client, message, link_number)
                    if modified_message is not None:
                        await forward_message(client, modified_message, CONFIGS.forward_as_copy,
                                              {target_id})
                except FloodWait as e:
                    print(f"FloodWait: {e.value} seconds")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    print(f"Error forwarding message: {str(e)}")
                    await client.send_message(chat_id="me",
                                              text=f"#ERROR: `{str(e)}`\n\nUnable to forward message to `{target_id}`")


if __name__ == "__main__":
    user.run()